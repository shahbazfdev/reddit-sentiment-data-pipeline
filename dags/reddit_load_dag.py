from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
from include.py_scripts.reddit_load import load_to_postgres

with DAG(
    dag_id="reddit_load_dag",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["reddit", "load"]
) as dag:

    load_task = PythonOperator(
        task_id="load_csv_to_postgres",
        python_callable=load_to_postgres
    )