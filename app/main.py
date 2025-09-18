import os
import streamlit as st
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain.document_loaders import TextLoader, PyPDFLoader, UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Prometheus imports
from prometheus_client import start_http_server, Counter, Histogram, Gauge, REGISTRY

# Load environment variables from .env
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# ─────────────── Prometheus Setup ───────────────
def get_or_create_metric(metric_type, name, documentation, **kwargs):
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]
    return metric_type(name, documentation, **kwargs)


if "prometheus_started" not in st.session_state:
    try:
        start_http_server(9001)
        st.session_state["prometheus_started"] = True
    except OSError as e:
        if "Address already in use" in str(e):
            st.warning("Prometheus metrics server already running on port 9001.")
            st.session_state["prometheus_started"] = True
        else:
            raise


# Metrics
queries_total = get_or_create_metric(Counter, 'total_queries', 'Total number of user queries', labelnames=["user"])
uploads_total = get_or_create_metric(Counter, 'total_uploads', 'Total number of document uploads', labelnames=["user"])
upload_failures_total = get_or_create_metric(Counter, 'upload_failures_total', 'Total failed document uploads', labelnames=["user"])
query_failures_total = get_or_create_metric(Counter, 'query_failures_total', 'Total failed user queries', labelnames=["user"])
retrieval_failures_total = get_or_create_metric(Counter, 'retrieval_failures_total', 'Total failed Pinecone retrievals', labelnames=["user"])
llm_failures_total = get_or_create_metric(Counter, 'llm_failures_total', 'Total failed LLM responses', labelnames=["user"])
upload_latency_seconds = get_or_create_metric(Histogram, 'upload_latency_seconds', 'Time taken to upload documents', labelnames=["user"])
query_latency_seconds = get_or_create_metric(Histogram, 'query_latency_seconds', 'End-to-end query latency (retrieval + LLM)', labelnames=["user"])
llm_latency_seconds = get_or_create_metric(Histogram, 'llm_latency_seconds', 'Time taken by LLM to generate a response', labelnames=["user"])
retrieval_latency_seconds = get_or_create_metric(Histogram, 'retrieval_latency_seconds', 'Time taken by Pinecone retrieval', labelnames=["user"])
document_chunks_uploaded = get_or_create_metric(
    Histogram, 'document_chunks_uploaded', 'Number of chunks generated per uploaded document batch',
    labelnames=["user"], buckets=[1, 10, 50, 100, 500, 1000, 5000]
)
queries_in_progress = get_or_create_metric(Gauge, 'queries_in_progress', 'Number of queries currently being processed', labelnames=["user"])
retrievals_in_progress = get_or_create_metric(Gauge, 'retrievals_in_progress', 'Number of retrievals currently being processed', labelnames=["user"])
llms_in_progress = get_or_create_metric(Gauge, 'llms_in_progress', 'Number of LLM generations currently being processed', labelnames=["user"])

# ─────────────── Document Handling ───────────────
def load_and_split_documents(folder_path):
    all_documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        extension = filename.lower().split(".")[-1]
        try:
            if extension == "txt":
                loader = TextLoader(file_path)
            elif extension == "pdf":
                loader = PyPDFLoader(file_path)
            elif extension in ["png", "jpg", "jpeg", "docx", "html", "eml"]:
                loader = UnstructuredFileLoader(file_path)
            else:
                continue
            documents = loader.load()
            all_documents.extend(documents)
        except Exception as e:
            st.error(f"Failed to load {filename}: {e}")

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return text_splitter.split_documents(all_documents)

def get_embeddings():
    return OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def init_pinecone():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT)
        )

@upload_latency_seconds.labels(user="anonymous").time()
def upload_documents_to_pinecone(docs, embeddings, user_id):
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        PineconeVectorStore.from_documents(docs, embedding=embeddings, index_name=PINECONE_INDEX_NAME)
        uploads_total.labels(user=user_id).inc()
        document_chunks_uploaded.labels(user=user_id).observe(len(docs))
        st.success(f"Uploaded {len(docs)} chunks to Pinecone.")
    except Exception as e:
        upload_failures_total.labels(user=user_id).inc()
        st.error(f"Upload failed: {e}")

# ─────────────── Query Handling ───────────────
def build_qa_chain():
    embeddings = get_embeddings()
    pc = Pinecone(api_key=PINECONE_API_KEY)
    vectorstore = PineconeVectorStore(embedding=embeddings, index_name=PINECONE_INDEX_NAME)

    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4", temperature=0.0)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    return qa_chain, vectorstore

@query_latency_seconds.labels(user="anonymous").time()
def query_with_llm(query_text, user_id):
    queries_in_progress.labels(user=user_id).inc()
    try:
        qa_chain, vectorstore = build_qa_chain()

        retrievals_in_progress.labels(user=user_id).inc()
        try:
            with retrieval_latency_seconds.labels(user=user_id).time():
                retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
                retrieved_docs = retriever.get_relevant_documents(query_text)
        except Exception as e:
            retrieval_failures_total.labels(user=user_id).inc()
            query_failures_total.labels(user=user_id).inc()
            st.error(f"Pinecone retrieval failed: {e}")
            return None
        finally:
            retrievals_in_progress.labels(user=user_id).dec()

        llms_in_progress.labels(user=user_id).inc()
        try:
            with llm_latency_seconds.labels(user=user_id).time():
                result = qa_chain({"query": query_text})
        except Exception as e:
            llm_failures_total.labels(user=user_id).inc()
            query_failures_total.labels(user=user_id).inc()
            st.error(f"LLM generation failed: {e}")
            return None
        finally:
            llms_in_progress.labels(user=user_id).dec()

        queries_total.labels(user=user_id).inc()
        return result

    except Exception as e:
        query_failures_total.labels(user=user_id).inc()
        st.error(f"Unexpected query pipeline failure: {e}")
        return None
    finally:
        queries_in_progress.labels(user=user_id).dec()

# ─────────────── Streamlit UI ───────────────
st.set_page_config(page_title="GenAI for Manufacturing", page_icon="🧠", layout="wide")

# Custom theme and footer styling
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; }

        .custom-title {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            color: #F5F5F5;
        }

        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background: #111;
            color: #999;
            text-align: center;
            padding: 10px;
            font-size: 0.85rem;
        }

        /* Optional: Make sidebar darker */
        section[data-testid="stSidebar"] {
            background-color: #161616;
        }

        /* Optional: Better contrast on main container */
        .main {
            background-color: #0E1117;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="custom-title">🧠 GenAI System for Manufacturing Applications</div>', unsafe_allow_html=True)
st.markdown("Built with Streamlit, LLM (gpt-4), LangChain, Pinecone, OpenAI, Prometheus, and Grafana")

# Layout
col1, col2 = st.columns([1, 2])

# ----- LEFT COLUMN -----
with col1:
    st.markdown("###  User Info")
    user_id = st.text_input("Enter your user ID", value="anonymous")

    st.markdown("### 📂 Upload Documents")
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

    if uploaded_files:
        os.makedirs("documents", exist_ok=True)
        for file in uploaded_files:
            file_path = os.path.join("documents", file.name)
            with open(file_path, "wb") as f:
                f.write(file.read())
        st.success("✅ Files uploaded successfully!")

    if st.button(" Process & Upload to Pinecone"):
        init_pinecone()
        docs = load_and_split_documents("documents")
        embeddings = get_embeddings()
        upload_documents_to_pinecone(docs, embeddings, user_id)

    with st.expander(" Reset Conversation"):
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared.")

# ----- RIGHT COLUMN -----
with col2:
    st.markdown("### 💬 Chat with Your Documents")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_query = st.chat_input("Type your question here...")

    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = query_with_llm(user_query, user_id)
                if result:
                    response = result["result"]
                    st.markdown(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})

                    with st.expander(" Source Documents"):
                        for i, doc in enumerate(result["source_documents"]):
                            st.markdown(f"**Source {i + 1}:**")
                            st.write(doc.page_content[:500] + "...")
                else:
                    error = "⚠️ Unable to generate a response."
                    st.markdown(error)
                    st.session_state.chat_history.append({"role": "assistant", "content": error})

# ----- Footer -----
st.markdown('<div class="footer">© Emmanuel Oyekanlu – All rights reserved</div>', unsafe_allow_html=True)
