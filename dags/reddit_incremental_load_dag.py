from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime
from pathlib import Path

SQL_DIR = Path("/usr/local/airflow/include/sql")

with DAG(
    dag_id="reddit_incremental_load_dag",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False,
    tags=["reddit", "postgres"],
) as dag:

    create_table = SQLExecuteQueryOperator(
        task_id="create_reddit_posts_table",
        conn_id="postgres_reddit",
        sql=(SQL_DIR / "create_reddit_posts.sql").read_text(),
    )

    incremental_load = SQLExecuteQueryOperator(
        task_id="incremental_load_unique_posts",
        conn_id="postgres_reddit",
        sql=(SQL_DIR / "incremental_load_reddit_posts.sql").read_text(),
    )

    create_table >> incremental_load