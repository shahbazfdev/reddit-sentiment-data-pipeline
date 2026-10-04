# include/py_scripts/reddit_transform.py
import pandas as pd
from pathlib import Path
from datetime import datetime
import os
from include.py_scripts.reddit_nlp import get_sentiment, detect_intent

RAW_DIR = Path("/usr/local/airflow/data/reddit/raw")
REFINED_DIR = Path("/usr/local/airflow/data/reddit/refined")
REFINED_DIR.mkdir(parents=True, exist_ok=True)

def transform_reddit_data():
    all_files = list(RAW_DIR.glob("reddit_raw_*.json"))
    if not all_files:
        print("No files found in raw directory")
        return None  # empty DF
    
    refined_source_file = f"reddit_transformed_{datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S')}.csv"

    dfs = []
    for file_path in all_files:
        print(f"Reading: {file_path}")
        try:
            df = pd.read_json(file_path)
        except ValueError:
            print(f"Skipping invalid JSON file: {file_path}")
            continue

        df["raw_source_file"] = file_path.name
        df["downvote_ratio"] = 1 - df.get("upvote_ratio", 0)
        df["sentiment"] = df["title"].apply(get_sentiment)
        df["intent"] = df["title"].apply(detect_intent)
        df["refined_source_file"] = refined_source_file

        # Convert timestamp
        df["date_posted"] = pd.to_datetime(df["created_utc"], unit="s").dt.strftime("%Y-%m-%d")
        df["time_posted"] = pd.to_datetime(df["created_utc"], unit="s").dt.strftime("%H:%M:%S")
        df["date_added"] = datetime.utcnow().date()
        df["time_added"] = datetime.utcnow().strftime("%H:%M:%S")

        # Select and reorder columns
        df = df[
            [
                "id", "subreddit", "title", "author", "score", "num_comments",
                "upvote_ratio", "downvote_ratio", "url", "sentiment", "intent",
                "date_posted", "time_posted", "date_added", "time_added", "raw_source_file", "refined_source_file"
            ]
        ]
        dfs.append(df)

    final_df = pd.concat(dfs, ignore_index=True)
    print(f"Final DataFrame shape: {final_df.shape}")
    print(final_df.head())

    output_file = REFINED_DIR / refined_source_file
    final_df.to_csv(output_file, index=False)
    print(f"Transformed CSV saved at {output_file}")