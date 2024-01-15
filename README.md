# Capstone Project Kelompok B  

# In this Repo
* Ingestion using airflow
* Transform and Load using DBT
* Visualization using Metabase

# Prerequirement
* Python and Virtual Environment
* Docker Compose
* Dbeaver

# Create Docker folder
In this step we make folder *Docker* for easier reading a file path. This folder contains Dockerfile and docker-compose.  
Dockerfile needed for installation of dbt; such as python image, update the systems, install various dependencies and tools for dbt, set environment, and dbt-postgres configuration.  
Docker-compose built for Apache-Airflow along with additional services; PostgreSQL, Redis, Docker proxy, and DBT, Metabase.    

this folder also contain with datasets that we get earlier from our mentor.

## Dataset
Since we are working on airflow, we need to ingest the dataset from local. So we moved them into dags folder.  
the dataset itself, have a csv and parquet type. for the csv file, we add the column to the right name using *read_data.py*, and for parquet we rename the column in the ingestion process.
there are the *dataset_name*_updated.csv file that have been modified.
The original dataset have 8 files, but we need to modify the 4 csv files. So total of the updated dataset in dags folder is 12 files.  

## Information for connection
### airflow metadata database connection:

* port    : 5436
* database: airflow
* username: airflow
* pass    : airflow

  
___
### airflow (http://localhost:8080/):
  
* username: airflow
* pass    : airflow
___  

### metabase database connection:
  
* port: 5432  
* database: metabase  
* username: metabase  
* pass: metabase  

___

### metabase (httpp://localhost:3000/):

* port: using `ipconfig` command, it's different every local
* username: ingest
* pass: ingest
* port_pg: 5445
* database: ingest

___

### warehouse database connection:

* port: 5445
* database: ingest
* username: ingest
* pass: ingest

___

## Run docker-compose by using:

`docker-compose up -d`  

There are total 12 container running on this docker-compose. The code can be see [here](https://github.com/ilyaslanang/capstone_project/blob/main/Docker/docker-compose.yml)  
After running this command, *dags* folder will be created, and we can start writing the code for ingestion inside that folder.  

___

## Make Virtual Environment  

After make sure docker is running well, 
run `python -m venv venv`
and run `pip install -r requirements.txt`  

___

## Airflow Configuration:

First, open [airflow](http://localhost:8080/)  

Fill the username and password with : `airflow`  

This is one of the example of the code [here](https://github.com/ilyaslanang/capstone_project/blob/main/Docker/dags/category.py)  
Add postgres connection in DAGs script and match it with configuration connection in airflow. 

![image](https://github.com/ilyaslanang/capstone_project/blob/main/documentations/connection_in%20airflow.png)

Write the *pg_conn_id* in the DAGs scripts then we must to take a look closely on the path in your local system for the dataset. It's important to aim the right path and connection.  

## Ingestion  

Writing DAGs scripts is the first step for ingestion process. Once it's done, you can run the scripts by using:  
`python3 category.py`  

This will pass to Dags in airflow dashboard.

![image](https://github.com/ilyaslanang/capstone_project/blob/main/documentations/airflow_dashboard.png)

Run it manually will trigger the ingestion into database we've prepared.  

After successfully ingest on airflow, the database *ingest* will look like this:  

![image](https://github.com/ilyaslanang/capstone_project/blob/main/documentations/database_ingest.png)

___


## Transform and Load

For this two step, DBT tools are used inside the airflow.    
We need to run this command:  
`dbt init`  
This command will trigger to create a profiles if you haven't one.  
Fill the configuration with this values:  
```
      user: ingest  
      password: ingest  
      dbname: ingest  
      host: host.docker.internal  
      port: 5445  
      schema: public  
      type: postgres  
```
 
or you can see the complete configuration in this [file](https://github.com/ilyaslanang/capstone_project/blob/main/dbt-profiles/profiles.yml)  

elsa yang lanjut buat dbt_project



### Running the DBT on airflow

Create DAG script [*dbt.py* ](https://github.com/ilyaslanang/capstone_project/blob/main/Docker/dags/dbt.py)  
This script define dbt debug, dbt run, and dbt test for airflow. Change the local path as the local system you are using.
Also, Docker-proxy is being used for connection in this script. run this command:  
`python3 dbt.py`  
This will pass to airflow dashboard. Run this manually will trigger the tasks.  

The result of the dbt test should be like this:  

![image](https://github.com/ilyaslanang/capstone_project/blob/main/documentations/dbt_logs.png)

and this is the database now:  

![image](https://github.com/ilyaslanang/capstone_project/blob/main/documentations/after%20dbt%20run%20in%20database.png)
