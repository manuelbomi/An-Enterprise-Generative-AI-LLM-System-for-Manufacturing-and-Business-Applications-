# An Enterprise Generative-AI LLM System for Manufacturing and Business Applications 


We present an enterprise large language model  (LLM) system that could be deployed by manufacturing and business leaders for manufacturing process analysis,  knowledge discovery, project assistance, and  manufacturing/business topic aggregation. The LLM system features a user interface (UI) that is similar to the ChatGPT UI through which manufacturing or business professionals can interact with, and query their own data warehoused as vector embeddings in a vector database (Pinecone). 

Open source <ins>**GE Vernova**</ins> and <ins>**GE Aerospace**</ins> datasets are used in this case study.

### The system is composed of the following core components:

<ins>**LangChain**</ins> – Manages orchestration and workflow across the system components.


<ins>**OpenAIEmbeddings**</ins>  – Converts enterprise manufacturing data into high-dimensional vector representations.

<ins>**GPT-4 (LLM)**</ins>  – Provides reasoning, natural language understanding, and advanced query handling.

<ins>**Pinecone Vector Database**</ins>  – Stores and indexes embeddings in the cloud to enable efficient similarity search and retrieval.

<ins>**Streamlit User Interface**</ins>  – Delivers an interactive, user-friendly frontend through which manufacturing leaders can query and analyze their vectorized enterprise datasets.

<ins>**Prometheus**</ins>  time series database and <ins>**Grafana**</ins>  are used as overall system performance monitoring tools. 

We also discuss how an Enterprise Architect may work alongside the Solution Architect to use MLOps (machine learning operations) best practices to scale up the system in an enterprise setting using MLOps and CI/CD orchestration tools such as ZenML, Kubeflow, Airflow and Kubernetes. 

### System Architecture 
The high-level system architecture and the system front end are displayed in the figures below:

---

<img width="831" height="381" alt="Image" src="https://github.com/user-attachments/assets/867b4609-af48-4afe-8242-9d521d62710f" />

---
### System Streamlit Front-End

Examples of how the system provide answers through the Streamlit front end are provided in the series of figures below:

#### Query: How does GE Vernova's top product delivers on 4R circulatory framework?

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/066931cc-5cb6-4733-900c-19449a2cc3d2" />

---

#### LLM System Response

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/7412f8cf-4215-4f47-a3b7-231586745752" />

---
### Further LLM system's response

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/7f457d46-be6b-4c7f-a4c0-77442155969a" />

---

####  Further LLM system's response

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/076095f7-c0cf-425a-a08b-bf50d8efa56b" />

---

#### Query: How does GE Aerospace contribute to defense and propulsion technologies? Cite references

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/2c086c66-62ec-48c2-85c7-bcc04e2fb81d" />

---

#### LLM System's response

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/be2751f2-da61-4c45-9717-e9ddaf2c670d" />

---

#### Further LLM system's  response

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/e5d3f08d-73d4-48e9-83ac-de5a4a0f95ed" />

---

#### Query: Is there any relationship between GE Vernova and GE Aerospace? 

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/14476f66-2876-4d06-8773-d9ce1c7cdd99" />


---

#### The Streamlit front end can be used for:

* Querying/interacting with the system (user interface)
* Uploading new data into the Pinecone vector database
* Displaying the result of the users' queries.


### Enterprise Data
The data warehoused in the Pinecone Vector database is an enterprise dataset since all forms of data (structured or unstructured) and most data formats (png, jpeg, txt, pdf, wav(sound), xml, docx, eml, wav html etc) can be chuncked and uploaded into the Pinecone vector database. 


### Monitoring System Performance with Prometheus and Grafana
Prometheus timeseries database is used to scrape important system metrics such as: 

##### Query Latencies

*  upload_latency_seconds → upload time

*  query_latency_seconds → full query time

*  retrieval_latency_seconds → Pinecone retrieval only

*  llm_latency_seconds → GPT generation only

  ##### File/Data Upload Failures

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

#### Grafana is used to display the results of metrics that are logged by Prometheus.

##### A figure showing query latency as logged by Prometheus is shown below:

---

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/021ebcd4-5531-440b-bfe2-53255cf42bba" />

---

##### A figure showing the LLM latency as captured  by Grafana from data logged by Prometheus  is shown below:

---

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/e18ce078-fd8a-47a3-8059-3fe6feff8670" />







# How to Deploy the Project for Manufacturing and other Enterprise Applications

The project can be deployed for numerous other enterprise applications even though this iteration is for manufacturing use case. To deploy for other applications, the enterprise dataset in the Pinecone vector database should be augmented to include the intended use case data.  As an example, a variant of the project for healthcare use case is available here: manuelbomi/An-Enterprise-LLM-System-for-HealthCare-Applications 

If the Solution Architect does not have access keys to a particular Pinecone database, the Solution Architect can just create a new index on Pinecone, and then warehouse the vector embeddings of the new dataset on the newly created Pinecone index.

Vector embeddings can be created by just clicking on the data to be uploaded via the Streamlit front end, and then clicking on <ins>**'Process and Upload to Pinecone'**</ins> button. The back end at main.py will efficiently handle data chunking and all other related Pinecone embedding processes. 

### Creating a Pinecone Vector Database
As mentioned earlier, to be able to deploy the solution for other applications in enterprise settings, the Solution Architect must first create a Pinecone database to store the vector embeddings of the dataset of the desired application. Infographs detailing how the Solution Architect may set up a free instance of the Pinecone vector database are provided below: 

---

#### Create a new index on Pinecone
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/9795a732-4745-457a-84c3-215e06007a1d" />

---

#### Click on Customs settings and set the vector dimension to 1536. (1536 is the OpenAI default vector length for most of OpenAI data embedding models)
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/d75d5dd2-546c-450e-818f-275e534413a1" />

---

#### Now, click to create the index
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/7116f7de-58c6-4eb5-aa99-97e5b0587eae" />

---

#### The new index will be available under the set of indexes available on your Pinecone homepage
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/c38337cf-0662-4675-bc4f-a9b95a17a1c8" />


### Setting up the project for On-Prem or Cloud Deployments
This project has been developed using VSCode on a Windows 10 enterprise system equipped with GeForce 3070 GPU. Without loss of generality, other types of commodity computers with other variants of operating systems can be used to reliably deploy the application. The project structure on VSCode can be set up as shown below: 

---

<img width="201" height="426" alt="Image" src="https://github.com/user-attachments/assets/c01b744a-9d89-4db4-aa8d-c881d2588524" />

---


To deploy the project, the Solution Engineer or Architect must clone the project from the Github repository here:   

A variant of the deployment for healthcare use case can also be cloned from here: manuelbomi/An-Enterprise-LLM-System-for-HealthCare-Applications 

---
#### Example of the main.py running on VSCode
After cloning, the project can be run using **docker-compose up --build** . The complete system (Streamlit + Prometheus + Grafana) should then be available on Docker. The Pinecone database is deployed on Pinecone cloud at [www.pinecone.io](https://app.pinecone.io). The Pinecone API key and the Pinecone Environment keys are used to connect the LLM system with the Pinecone vector database. 


OpenAI API key is used to obtain key that facilitate the usage of OpenAPI Embeddings. Langchain is used to connect the OpenAPI Embedding and the vectorized healthcare data to the Pinecone vector database. An example of the project back end running on VSCode is shown in the figure below:

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/4ede62a2-7903-43f0-b916-a4dc732de390" />

---

> [!IMPORTANT]
> ### To run the project successfully, Docker must be available and running on the local system before the **docker-compose up --build** command
> ### Virtual environment should be created on VSCode for the project, and it must be activated prior to running the project.
> ### The .env file must be on the same directory as the main.py. The .env file must contain the Pinecone API key, the OpenAI API key, the Pinecone Environment, and Pinecone Index Name
> ### The .gitignore must be in the root directory and it must contain the virtual environment name and the .env so that when the Solution Architect pushes the solution onto Github to be deployed, the secrets in the .env file and the huge virtual environment folder will not be pushed. 

---

#### On Prem-Deployment
After deploying the solution with **docker-compose up --build** command, major front-end components of the projects (Streamlit, Prometheus & Grafana) will be available at the following URLs:

- <ins>**Streamlit**</ins> will be available
 at http://localhost:8501/  or any other port or URL that the Solution Architect designates in the docker-compose.yml file
  
- <ins>**Prometheus**</ins> will be available at http://localhost:9090/  or any other port or URL that the Solution Architect designates in the docker-compose.yml file
  
- <ins>**Grafana**</ins> will be available at http://localhost:3006/  or any other port or URL that the Solution Architect designates in the docker-compose.yml file

#### Cloud Deployment
For production grade deployments, a dockerized version of the project should be created by the Solution Architect and stored in the enterprise Docker Hub. Other alternatives such as Github Containers or AWS ECR (Elastic Container Registry) can also be considered. 

The solution can then be deployed via a .github/workflow yaml jobs onto a cloud platform such as GCP Apps Engine, Azure Web Apps, Azure Kubernets Services (AKS), GCP Cloud Run etc. 



### Scaling Up for Enterprise Applications
#### Using Callable Functions
The Enterprise Architect may desire to deploy the system for other use cases in the enterprise. It is observable that a significant portion of the code in main.py is encapsulated within callable functions. Using callable functions will enable the Solution or Enterprise Architect to easily deploy the system for other applications. Also, using callable functions is fundamental to good MLOps and CI/CD pratices. With callable functions, adjustements or adding new features to the project can easily be accomplished. Also, productionising the system will be easy and robust after any adjustment or new feature addition.  

#### Using ZenML or Airflow for MLOps
Orcestration tools such as ZenML or Airflow can be used together with CI/CD tools such as Github Actions. Using ZenML or Airflow will aid robust MLOps strategies across the enterprise. 

#### Kubeflow for deploying on Kubernetes 
As usesrs of the system increases, there may be a need to scale up the number of Kubernetes pods and Docker nodes that are used in production. Using tools such as Kubeflow as orchestrating tool will enable such scaling up to be easily achieved. This will lead to a very reactive and robust system that seamlessly serves its enterprise objectives.   








--
Thank you for reading through

---
### **AUTHOR'S BACKGROUND**
### Author's Name:  Emmanuel Oyekanlu
```
Skillset:   I have experience spanning several years in data science, developing scalable enterprise data pipelines,
enterprise solution architecture, architecting enterprise systems data and AI applications,
software and AI solution design and deployments, data engineering, high performance computing (GPU, CUDA), machine learning,
NLP, Agentic-AI and LLM applications as well as deploying scalable solutions (apps) on-prem and in the cloud.

I can be reached through: manuelbomi@yahoo.com

Website:  http://emmanueloyekanlu.com/
Publications:  https://scholar.google.com/citations?user=S-jTMfkAAAAJ&hl=en
LinkedIn:  https://www.linkedin.com/in/emmanuel-oyekanlu-6ba98616
Github:  https://github.com/manuelbomi

```
[![Icons](https://skillicons.dev/icons?i=aws,azure,gcp,scala,mongodb,redis,cassandra,kafka,anaconda,matlab,nodejs,django,py,c,anaconda,git,github,mysql,docker,kubernetes&theme=dark)](https://skillicons.dev)














































































