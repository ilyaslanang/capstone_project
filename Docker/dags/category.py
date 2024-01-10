from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import os
import pandas as pd

with DAG(
    dag_id="ingestion_category",
    schedule=None,
    start_date=datetime(2023, 12, 31),
    catchup=False
) as dag:
    
    def load_data(file_path):
        if os.name == 'nt':
            file_path = file_path.replace('/', '\\')
        data = pd.read_csv(file_path)

        return data

    def create_table(**kwargs):
        file_path = '/opt/airflow/dags/dataset/product_category_updated.csv'
        data = load_data(file_path)
        sql = """
        CREATE TABLE IF NOT EXISTS product_category (
            category_id INTEGER PRIMARY KEY,
            nama_kategori VARCHAR(50)
        )
        """
        pg_hook = PostgresHook(postgres_conn_id='pg_conn_id')
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()

        for index, row in data.iterrows():
            cursor.execute("""
            INSERT INTO product_category (category_id, nama_kategori)
            VALUES (%s, %s)
        """, (row["category_id"], row["nama_kategori"]))
        
        conn.commit()

    create_table_task = PythonOperator(
        task_id='ingestion_for_capstone',
        python_callable=create_table,
        dag=dag,
    )

    create_table_task