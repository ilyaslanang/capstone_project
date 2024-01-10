from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import os
import pandas as pd

with DAG(
    dag_id="ingestion_customer",
    schedule=None,
    start_date=datetime(2023, 12, 31),
    catchup=False
) as dag:
    
    def load_data(file_path):
        if os.name == 'nt':
            file_path = file_path.replace('/', '\\')
        data = pd.read_parquet(file_path)

        data.rename(columns={'column0': 'customer_id', 'column1': 'nama_pelanggan', 'column2': 'alamat_pelanggan'}, inplace=True)
        return data

    def create_table(**kwargs):
        file_path = '/opt/airflow/dags/dataset/Customer.parquet'
        data = load_data(file_path)
        sql = """
        CREATE TABLE IF NOT EXISTS customer (
            customer_id INTEGER PRIMARY KEY,
            nama_pelanggan VARCHAR(100),
            alamat_pelanggan VARCHAR(100)
        )
        """
        pg_hook = PostgresHook(postgres_conn_id='pg_conn_id')
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()

        for index, row in data.iterrows():
            cursor.execute("""
            INSERT INTO customer (customer_id, nama_pelanggan, alamat_pelanggan)
            VALUES (%s, %s, %s)
        """, (row["customer_id"], row["nama_pelanggan"], row["alamat_pelanggan"]))
        
        conn.commit()



    create_table_task = PythonOperator(
        task_id='ingestion_for_capstone',
        python_callable=create_table,
    )

    create_table_task