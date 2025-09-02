<<<<<<< HEAD
# An Enterprise LLM System for HealthCare Applications
"# An-Enterprise-LLM-System-for-Healthcare-Applications-b" 
=======
# An Enterprise LLM System for Healthcare Applications

We present an enterprise LLM system that could be deployed by healthcare practitioners for knowledge discovery, project assistance, and  healthcare topic aggregation. The LLM system present an interface that is similar to the ChatGPT interface through which healthcare professionals can interact with their own data warehoused as vector embeddings in a vector database (Pinecone). 

The system imploy the use of Langchain, OpenAIEmbeddings and Pinecove vector database to convert healthcare enterprise data into vector embeddings using OpenAIEmbeddings. The vector embeddings are stored in a Pinecone Cloud vector database. Streamlit is used to provide a friendly user interface through which healthcare practitioners can interact with their vectorised enterprise datasets. Prometheus time series database and Grafana are used as overall system performance monitoring tools. 

### System Architecture 
The high-level system architecture and the system front end are displayed in the figures below:

---

<img width="521" height="301" alt="Image" src="https://github.com/user-attachments/assets/db8beb9c-c908-4247-8a01-d715d6b72159" />

---
### System Streamlit Front-End
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/2d785f47-8aa3-4471-86bc-444d663c7372" />

---

### Enterprise Data
The data warehoused in the Pinecone Vector database is an enterprise dataset since all forms of data (structure or unstructured) and most data formats (png, jpeg, txt, pdf, wav(sound), xml, docx, eml, wav html etc) can be chuncked and uploaded into the 
into the Pinecone vector database. 

### Streamlit Front End
The Streamlit front end can be used for:

* Querying/interacting with the system (user interface)
* Uploading new data into the Pinecone vector database
* Displaying the result of the users' queries.

### Montoring System Performance with Prometheus and Grafana
Prometheus timeseries database is used to scrape important system metrics such as 

##### Latency

*  upload_latency_seconds → upload time

*  query_latency_seconds → full query time

*  retrieval_latency_seconds → Pinecone retrieval only

*  llm_latency_seconds → GPT generation only

  ##### Failures

*  upload_failures_total

*  retrieval_failures_total

*  llm_failures_total

*  query_failures_total

##### System Concurrency

* queries_in_progress

*  retrievals_in_progress

*  llms_in_progress

*  Document Size

*  document_chunks_uploaded (histogram of how many chunks each doc upload produced)

  ##### Users' Related Metrics

* total_queries{user="emmanuel"}

* query_latency_seconds_bucket{user="anonymous"}

* document_chunks_uploaded_sum{user="emmanuel"}


Grafana is used to display the results of Prometheus metrics.

### System Deployment (Docker)

The complete system (Streamlit + Prometheus + Grafana) is deployed on a Docker network. The Pinecone database is deployed on Pinecone cloud at [www.pinecone.io](https://app.pinecone.io). The Pinecone API key and the Pinecone Environment keys are used to connect the local system with the Pinecone vector database. 

OpenAI API key is used to obtain key that facilitate the usage of OpenAPI Embeddings. Landchain is used to connect the OpenAPIEmbedding and the vectorized healthcare data to the Pinecone vc=ector database. 



### How to Deploy for Enterprise Applications

The project can be deployed for numerous enterprise applications even though this iteration is for health-care uses. To deploy for other applications, only the enterprise dataset in the Pinecone vector database should be changed. For example, a use case of the same applications for manufacturing is available here: 

To deploy for other applications in industrial settings, the Solution Engineer must first create a Pinecone databases that warehouses the vector embeddings of the dataset of the desired application. An infograph tutorial on how to set up a free instance of the Pinecone vector database is available here: 

#### Setting up the project locally
This project has been developed using VSCode on a Windows 10 based enterprise system equipped with GeForce 3070 GPU. Without loss of generality, other types of commodity computers with other variants of operating systems can be used to deploy the application. The project structure on VSCode can be set up as shown below: 

---

<img width="225" height="458" alt="Image" src="https://github.com/user-attachments/assets/c28967a2-167f-42a3-909e-f1a190624cf4" />
---

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/8805177c-fbea-4481-8414-82395a17f256" />

---

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/0ab1a93e-74e9-4080-8271-d57707f6d87d" />

---

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/5b588f6d-2336-4c3d-821e-66b961fae90c" />

---

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/e84b4423-1165-4209-9ffc-b88f867f2ab8" />

---

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/5f226b98-4a50-4d81-8bc9-e97b2da1ad7b" />

---

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/fe1f48e8-e941-4474-9a51-074bfa84e246" />

---

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/1708aec5-67d1-4e95-9e80-c9c5e702dbf8" />

---

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/12ef7201-1a5d-4d46-8884-7219d018f5f8" />

---

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/e3393cf5-f00f-4567-ad51-e3f7171c2a82" />

---

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/baf76756-7e74-4aae-ab44-de3172d495cb" />

---

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/268cb56b-4c03-443a-b59b-d08b15e14da3" />

---

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/26b112f6-40c2-4ac2-b6d8-8e8a581181ad" />

---
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/d57c65d5-7631-46e8-b05f-79e69024a770" />

---
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/bb2af9cd-e830-428d-ab65-972b5ce15573" />

---
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/d21e0858-cb82-4deb-b1f5-ecd10de57b46" />

---
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/d3cac355-9e48-4e95-af6a-4724ac28f74f" />


--- 
### Scaling Up for Enterprise Applications
#### Callable Functions

#### ZenML (MLOps)

#### Kubeflow for deploying on Kubernetes 








--
Thank you for reading through

---
### **AUTHOR'S BACKGROUND**
### Author's Name:  Emmanuel Oyekanlu
```
Skillset:   I have experience spanning several years in developing scalable enterprise data pipelines,
data science applications, enterprise solution architecture, architecting enterprise systems data and AI applications,
software and AI solution design and deployments, data engineering, high performance computing (GPU, CUDA), machine learning,
NLP and LLM applications as well as deploying scalable solutions (apps) on-prem and in the cloud.

I can be reached through: manuelbomi@yahoo.com

Website:  http://emmanueloyekanlu.com/
Publications:  https://scholar.google.com/citations?user=S-jTMfkAAAAJ&hl=en
LinkedIn:  https://www.linkedin.com/in/emmanuel-oyekanlu-6ba98616
Github:  https://github.com/manuelbomi

```
[![Icons](https://skillicons.dev/icons?i=aws,azure,gcp,scala,mongodb,redis,cassandra,kafka,anaconda,matlab,nodejs,django,py,c,anaconda,git,github,mysql,docker,kubernetes&theme=dark)](https://skillicons.dev)
>>>>>>> 64a231af6d953b967a93a9c3dc4b5f052de76119
