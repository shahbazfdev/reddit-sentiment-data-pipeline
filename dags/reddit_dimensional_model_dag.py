from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime
from pathlib import Path

SQL_DIR = Path("/usr/local/airflow/include/sql")

with DAG(
    dag_id="reddit_dimensional_model_dag",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False,
    tags=["reddit", "postgres", "dimensional"],
) as dag:

    dim_subreddit = SQLExecuteQueryOperator(
        task_id="load_dim_subreddit",
        conn_id="postgres_reddit",
        sql=(SQL_DIR / "dim_subreddit.sql").read_text(),
    )

    dim_author = SQLExecuteQueryOperator(
        task_id="load_dim_author",
        conn_id="postgres_reddit",
        sql=(SQL_DIR / "dim_author.sql").read_text(),
    )

    dim_raw_file = SQLExecuteQueryOperator(
        task_id="load_dim_raw_source_file",
        conn_id="postgres_reddit",
        sql=(SQL_DIR / "dim_raw_source_file.sql").read_text(),
    )

    dim_refined_file = SQLExecuteQueryOperator(
        task_id="load_dim_refined_source_file",
        conn_id="postgres_reddit",
        sql=(SQL_DIR / "dim_refined_source_file.sql").read_text(),
    )

    fact_posts = SQLExecuteQueryOperator(
        task_id="load_fact_reddit_posts",
        conn_id="postgres_reddit",
        sql=(SQL_DIR / "fact_reddit_posts.sql").read_text(),
    )

    [
        dim_subreddit,
        dim_author,
        dim_raw_file,
        dim_refined_file,
    ] >> fact_posts