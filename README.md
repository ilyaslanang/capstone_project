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

### metabase (http://localhost:3000/):

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


We need to run this command to install package.yml which is used to run dbt expectation. It aims to test the data warehouse that has been created:  
`dbt deps`  
You can see the complete configuration in this [*package.yml* ](https://github.com/ilyaslanang/capstone_project/blob/main/dbt_project/packages.yml)

# Data Model 1


`(expired_date - production_date) AS usia_hari` This expression calculates the age of the product in days. Subtracting the production date from the expiration date gives the number of days the product has been in existence.

The `FROM` statement specifies the data source table used for information extraction. Here, the source table is mentioned using the notation `{{ ref('stg_product') }}`. This indicates that a source table named `stg_product` will be used. The `{{ ref(...) }}` notation is dbt's way of referring to tables or other dbt models in a project.

You can see the complete configuration in this [*fct_product_age.sql*](https://github.com/ilyaslanang/capstone_project/blob/main/dbt_project/models/dbt-fct/fct_product_age.sql)

# Data Model 2

`COALESCE(count(stg_product.category_id), 0) AS product_count` This is a `COUNT` aggregation function that counts the number of products in each category. The `COALESCE` function is used to replace the NULL value with 0 if no products are found in the category.

`COALESCE(AVG((expired_date - production_date)), 0) AS average_product_age` This is an `AVG` aggregation function that calculates the average age of products in each category. The `COALESCE` function is also used here to replace NULL values ​​with 0 if no age data is available.

`COALESCE(sum(sales_amount), 0) as sales_amount` This is a `SUM` aggregation function that calculates total sales in each category. The `COALESCE` function is used to replace NULL values ​​with 0 if no sales data is available.

`LEFT JOIN` Performs a join with the LEFT JOIN type, which will return all rows from the left table `(stg_productcategory)` and matching rows from the right table `(stg_product)`. If there is no correspondence, the columns of the right table will be filled with NULL values.

`ON stg_product.category_id = stg_productcategory.category_id` Specifies merge conditions based on the category_id column. Two other joins are performed on the stg_transaction table using the product_id column as the key.

`GROUP BY nama_kategori` This script groups query results based on the category_name column. This is necessary because we perform aggregation operations (COUNT, AVG, SUM) at the category level. As a result, each row in the results will represent a single category with corresponding aggregation statistics.

You can see the complete configuration in this [*fct_category_statistic.sql*](https://github.com/ilyaslanang/capstone_project/blob/main/dbt_project/models/dbt-fct/fct_category_statistic.sql)

# Data Model 3

`LEFT JOIN` Performs a join with the LEFT JOIN type, which will return all rows from the left table `(stg_stock)` and matching rows from the right table `(stg_product)`. If there is no correspondence, the columns of the right table will be filled with NULL values.

`ON stg_product.product_id = stg_stock.product_id` Specifies the merge condition based on the product_id column

`ORDER BY product_id` This clause sorts query results based on the product_id column in ascending order (default). So, the results will be sorted by product ID.

You can see the complete configuration in this [*fct_available_stock.sql*](https://github.com/ilyaslanang/capstone_project/blob/main/dbt_project/models/dbt-fct/fct_available_stock.sql)

# Data Model 4

`LEFT JOIN` Performs a join with the LEFT JOIN type, which will return all rows from the left table `(stg_transaction)` and matching rows from the right table `(stg_product)`. If there is no correspondence, the columns of the right table will be filled with NULL values.

`ON stg_product.product_id = stg_transaction.product_id` Specifies the merge condition based on the product_id column.

`ORDER BY transaction_id` This clause sorts query results based on the `transaction_id` column in ascending order (default). So, the results will be sorted based on transaction ID.

You can see the complete configuration in this [*fct_transaction_product.sql*](https://github.com/ilyaslanang/capstone_project/blob/main/dbt_project/models/dbt-fct/fct_transaction_product.sql)

# Data Model 5

This entire query retrieves two columns (date and transaction_amount) from the stg_transaction table. The column names and aliases provided are only names for query results and do not affect the data retrieved from the table.

You can see the complete configuration in this [*fct_time_analysis.sql*](https://github.com/ilyaslanang/capstone_project/blob/main/dbt_project/models/dbt-fct/fct_time_analysis.sql)

# Schema of the Data Model

The explanation below covers all models:

Model `fct_product_age` :
Description: Staging model for product age.


The columns include (columns):

* `Product_id` : product ID (Primary Key).
* `Nama_produk` : Product name.
* `usia_hari` : Product age in days.


The test include (tests):

`dbt_expectations.expect_table_row_count_to_equal_other_table` : Checks the row count of this model and compares it to the row count of the stg_product table or model. Some optional parameters are used such as group_by, compare_group_by, factor, row_condition, and compare_row_condition.

You can see the complete configuration in this [*schema.yml*](https://github.com/ilyaslanang/capstone_project/blob/main/dbt_project/models/dbt-fct/schema.yml)

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
