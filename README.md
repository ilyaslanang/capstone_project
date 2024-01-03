# Capstone Project Kelompok B
# In this Repo
* Ingestion using airflow
* Transform using DBT
* Load
* Visualization using Metabase

# Prerequirement
* Python and Virtual Environment
* Docker Compose

# Create Docker folder
In this step we make folder *Docker* for easier reading a file path. This folder contains Dockerfile and docker-compose.  
Dockerfile needed for installation of dbt; such as python image, update the systems, install various dependencies and tools for dbt, set environment, and dbt-postgres configuration.  
Docker-compose built for Apache-Airflow along with additional services; PostgreSQL, Redis, Flower, Docker proxy, and dbt.  

this folder also contain with datasets that we get earlier from our mentor.

## Dataset
since we are working on airflow, we need to ingest the dataset from local. So we moved them into dags folder.

# Ingestion
* first, make the environment:  
`python -m venv venv`

### Information for connection
* postgres connection:  
`
 host    : localhost  
 port    : 5432  
 database: airflow  
 username: airflow  
 pass    : airflow
`
* airflow ([airflow](http://localhost:8080/):  
`
username: airflow  
pass    : airflow
`

* run docker-compose by using:

`docker-compose up -d`
after running this command, *dags* folder will be created, and we can start writing the code for ingestion.
