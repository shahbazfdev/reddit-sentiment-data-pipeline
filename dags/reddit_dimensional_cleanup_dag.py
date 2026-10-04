from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime
from pathlib import Path

SQL_DIR = Path("/usr/local/airflow/include/sql")

with DAG(
    dag_id="reddit_dimensional_cleanup_dag",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False,
    tags=["reddit", "postgres", "cleanup"],
) as dag:

    create_table = SQLExecuteQueryOperator(
        task_id="truncate_dim_fact_tables",
        conn_id="postgres_reddit",
        sql=(SQL_DIR / "cleanup_dimensional_tables.sql").read_text(),
    )