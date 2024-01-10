from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import os
import pandas as pd

with DAG(
    dag_id="ingestion_stock",
    schedule=None,
    start_date=datetime(2023, 12, 31),
    catchup=False
) as dag:
    
    def load_data(file_path):
        if os.name == 'nt':
            file_path = file_path.replace('/', '\\')
        data = pd.read_parquet(file_path)

        data.rename(columns={'column0': 'stock_id', 'column1': 'product_id', 'column2': 'jumlah_stok', 'column3': 'lokasi_gudang'}, inplace=True)
        return data

    def create_table(**kwargs):
        file_path = '/opt/airflow/dags/dataset/stock.parquet'
        data = load_data(file_path)
        sql = """
        CREATE TABLE IF NOT EXISTS Stock (
            stock_id INTEGER PRIMARY KEY,
            product_id INTEGER,
            jumlah_stok INTEGER,
            lokasi_gudang VARCHAR(100)
        )
        """
        pg_hook = PostgresHook(postgres_conn_id='pg_conn_id')
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()

        for index, row in data.iterrows():
            cursor.execute("""
            INSERT INTO Stock (stock_id, product_id, jumlah_stok, lokasi_gudang)
            VALUES (%s, %s, %s, %s)
        """, (row["stock_id"], row["product_id"], row["jumlah_stok"], row["lokasi_gudang"]))
        
        conn.commit()



    create_table_task = PythonOperator(
        task_id='ingestion_for_capstone',
        python_callable=create_table,
    )

    create_table_task