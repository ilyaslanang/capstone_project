from airflow import DAG
from datetime import datetime
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python import PythonOperator
import json
import pandas as pd

with DAG(
    dag_id="ingestion_capstone",
    schedule_interval=None,
    start_date=datetime(2023, 12, 31),
    catchup=False
) as dag:
    
    def load_data(file_path):
        data = pd.read_parquet(file_path)
        return data

    def create_table(**kwargs):
        file_path = r"C:\Users\acer\Desktop\DE\capstone\capstone_brief\Dataset\Customer.parquet"
        data = load_data(file_path)
        sql = """
        CREATE TABLE IF NOT EXISTS raw_table (
            id_customer INTEGER,
            customer_name VARCHAR(100),
            customer_address VARCHAR(100)
        )
        """
        pg_hook = PostgresHook(postgres_conn_id='pg_conn_id')
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()

        cursor.executemany("""
            INSERT INTO raw_table (id_customer, customer_name, customer_address)
            VALUES (%s, %s, %s)
        """, (
            (item["id_customer"], item["customer_name"], item["customer_address"])
        )
        )
        conn.commit()



    create_table_task = PythonOperator(
        task_id='create_table',
        python_callable=create_table,
        provide_context=True,
    )

    create_table_task