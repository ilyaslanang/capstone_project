from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import os
import pandas as pd

with DAG(
    dag_id="ingestion_product",
    schedule=None,
    start_date=datetime(2023, 12, 31),
    catchup=False
) as dag:
    
    def load_data(file_path):
        if os.name == 'nt':
            file_path = file_path.replace('/', '\\')
        data = pd.read_parquet(file_path)

        data.rename(columns={'column0': 'product_id', 'column1': 'nama_produk', 'column2': 'tanggal_produksi', 'column3': 'tanggal_kedaluwarsa', 'column4': 'category_id', 'column5': 'supplier_id'}, inplace=True)
        return data

    def create_table(**kwargs):
        file_path = '/opt/airflow/dags/dataset/product.parquet'
        data = load_data(file_path)
        sql = """
        CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY,
            nama_produk VARCHAR(200),
            tanggal_produksi DATE,
            tanggal_kedaluwarsa DATE,
            category_id INTEGER,
            supplier_id INTEGER
        )
        """
        pg_hook = PostgresHook(postgres_conn_id='pg_conn_id')
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()

        for index, row in data.iterrows():
            cursor.execute("""
            INSERT INTO product (product_id, nama_produk, tanggal_produksi, tanggal_kedaluwarsa, category_id, supplier_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row["product_id"], row["nama_produk"], row["tanggal_produksi"], row["tanggal_kedaluwarsa"], row["category_id"], row["supplier_id"]))
        
        conn.commit()



    create_table_task = PythonOperator(
        task_id='ingestion_for_capstone',
        python_callable=create_table,
    )

    create_table_task