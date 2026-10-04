CREATE TABLE IF NOT EXISTS dim_subreddit (
    subreddit_id SERIAL PRIMARY KEY,
    subreddit_name TEXT UNIQUE NOT NULL
);

INSERT INTO dim_subreddit (subreddit_name)
SELECT DISTINCT subreddit
FROM reddit_posts
WHERE subreddit IS NOT NULL
ON CONFLICT (subreddit_name) DO NOTHING;