from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import os
import pandas as pd

with DAG(
    dag_id="ingestion_transaction",
    schedule=None,
    start_date=datetime(2023, 12, 31),
    catchup=False
) as dag:
    
    def load_data(file_path):
        if os.name == 'nt':
            file_path = file_path.replace('/', '\\')
        data = pd.read_parquet(file_path)

        data.rename(columns={'column0': 'transaction_id', 'column1': 'product_id', 'column2': 'jumlah_pembelian', 'column3': 'jumlah_penjualan', 'column4': 'tanggal_transaksi'}, inplace=True)
        return data

    def create_table(**kwargs):
        file_path = '/opt/airflow/dags/dataset/transaction.parquet'
        data = load_data(file_path)
        sql = """
        CREATE TABLE IF NOT EXISTS transaction (
            transaction_id INTEGER PRIMARY KEY,
            product_id INTEGER,
            jumlah_pembelian INTEGER,
            jumlah_penjualan INTEGER,
            tanggal_transaksi DATE
        )
        """
        pg_hook = PostgresHook(postgres_conn_id='pg_conn_id')
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()

        for index, row in data.iterrows():
            cursor.execute("""
            INSERT INTO transaction (transaction_id, product_id, jumlah_pembelian, jumlah_penjualan, tanggal_transaksi)
            VALUES (%s, %s, %s, %s, %s)
        """, (row["transaction_id"], row["product_id"], row["jumlah_pembelian"], row["jumlah_penjualan"], row["tanggal_transaksi"]))
        
        conn.commit()



    create_table_task = PythonOperator(
        task_id='ingestion_for_capstone',
        python_callable=create_table,
    )

    create_table_task