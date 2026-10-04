from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
from include.py_scripts.reddit_extractor import extract_raw_reddit_data, extract_and_save

with DAG(
    dag_id="reddit_extract_dag",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["reddit", "extract"]
) as dag:

    extract_task = PythonOperator(
        task_id="extract_and_save",
        python_callable=extract_and_save
    )