from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime
from include.py_scripts.reddit_cleanup_files import cleanup_raw_files, cleanup_refined_files
from pathlib import Path

SQL_DIR = Path("/usr/local/airflow/include/sql")

with DAG(
    dag_id="reddit_cleanup_dag",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["reddit", "cleanup"]
) as dag:

    cleanup_raw = PythonOperator(
        task_id="cleanup_raw_files",
        python_callable=cleanup_raw_files
    )

    cleanup_refined = PythonOperator(
        task_id="cleanup_refined_files",
        python_callable=cleanup_refined_files
    )

    cleanup_staging = SQLExecuteQueryOperator(
        task_id="cleanup_stg_reddit_posts",
        conn_id="postgres_reddit",
        sql=(SQL_DIR / "cleanup_stg_reddit_posts.sql").read_text()
    )

    cleanup_raw >> cleanup_refined >> cleanup_staging