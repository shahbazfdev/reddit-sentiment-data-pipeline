from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
from include.py_scripts.reddit_transform import transform_reddit_data

with DAG(
    dag_id="reddit_transform_dag",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["reddit", "transform"]
) as dag:

    transform_task = PythonOperator(
        task_id="transform_reddit_data",
        python_callable=transform_reddit_data
    )