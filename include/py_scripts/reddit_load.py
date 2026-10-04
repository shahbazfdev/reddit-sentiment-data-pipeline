from airflow.hooks.base import BaseHook
from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path

REFINED_DIR = Path("/usr/local/airflow/data/reddit/refined")

def load_to_postgres():
    all_files = list(REFINED_DIR.glob("reddit_transformed_*.csv"))
    if not all_files:
        print("No CSV files found in refined directory")
        return

    # Get Airflow connection
    conn = BaseHook.get_connection("postgres_reddit")
    engine = create_engine(
        f"postgresql+psycopg2://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
    )

    for file_path in all_files:
        print(f"Loading file: {file_path}")
        df = pd.read_csv(file_path)

        # Load into Postgres, replace table if exists
        df.to_sql("stg_reddit_posts", engine, if_exists="append", index=False)
        print(f"Loaded {len(df)} rows from {file_path} into Postgres")