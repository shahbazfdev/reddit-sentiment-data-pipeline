import praw
from datetime import datetime
import json
import os
from airflow.sdk.bases.hook import BaseHook
from airflow.models import Variable

def extract_raw_reddit_data():
    conn = BaseHook.get_connection("reddit_api")
    reddit = praw.Reddit(
        client_id=conn.login,
        client_secret=conn.password,
        user_agent=conn.extra_dejson.get("user_agent")
    )

    REDDIT_CONFIG = Variable.get(
    "reddit_config",
    deserialize_json=True
    )

    all_posts = []
    
    for subreddit_name in REDDIT_CONFIG["subreddits"]:
        subreddit = reddit.subreddit(subreddit_name)

        if REDDIT_CONFIG["post_type"] == "new":
            posts = subreddit.new(limit=REDDIT_CONFIG["limit"])
        elif REDDIT_CONFIG["post_type"] == "hot":
            posts = subreddit.hot(limit=REDDIT_CONFIG["limit"])
        else:
            posts = subreddit.top(limit=REDDIT_CONFIG["limit"])

        for post in posts:
            all_posts.append({
                "id": post.id,
                "subreddit": subreddit_name,
                "title": post.title,
                "created_utc": post.created_utc,
                "author": str(post.author) if post.author else None,
                "score": post.score,
                "upvote_ratio": post.upvote_ratio,
                "num_comments": post.num_comments,
                "url": post.url,
                "extracted_at": datetime.utcnow().isoformat()
            })

    return all_posts

RAW_DIR = "/usr/local/airflow/data/reddit/raw"

def extract_and_save():
    os.makedirs(RAW_DIR, exist_ok=True)

    ts = datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")
    file_path = f"{RAW_DIR}/reddit_raw_{ts}.json"

    posts = extract_raw_reddit_data()

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)

    print(f"Saved {len(posts)} posts to {file_path}")