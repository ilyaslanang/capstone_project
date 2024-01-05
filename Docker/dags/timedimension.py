from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import os
import pandas as pd

with DAG(
    dag_id="ingestion_timed",
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
        file_path = '/opt/airflow/dags/dataset/timedimension_updated.csv'
        data = load_data(file_path)
        sql = """
        CREATE TABLE IF NOT EXISTS time_dimension (
            date_id INTEGER PRIMARY KEY,
            tanggal DATE,
            bulan INTEGER,
            tahun INTEGER
        )
        """
        pg_hook = PostgresHook(postgres_conn_id='pg_conn_id')
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()

        for index, row in data.iterrows():
            cursor.execute("""
            INSERT INTO time_dimension (date_id, tanggal, bulan, tahun)
            VALUES (%s, %s, %s, %s)
        """, (row["date_id"], row["tanggal"], row["bulan"], row["tahun"]))
        
        conn.commit()



    create_table_task = PythonOperator(
        task_id='ingestion_for_capstone',
        python_callable=create_table,
    )

    create_table_task