CREATE TABLE IF NOT EXISTS fact_reddit_posts (
    fact_id BIGSERIAL PRIMARY KEY,

    post_id TEXT UNIQUE NOT NULL,   -- natural key (from reddit)

    subreddit_id INT NOT NULL,
    author_id INT,
    raw_source_file_id INT,
    refined_source_file_id INT,

    score INT,
    num_comments INT,
    upvote_ratio FLOAT,
    downvote_ratio FLOAT,

    sentiment TEXT,
    intent TEXT,

    post_created_ts TIMESTAMP NOT NULL,
    record_loaded_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO fact_reddit_posts (
    post_id,
    subreddit_id,
    author_id,
    raw_source_file_id,
    refined_source_file_id,
    score,
    num_comments,
    upvote_ratio,
    downvote_ratio,
    sentiment,
    intent,
    post_created_ts
)
SELECT
    rp.id AS post_id,
    ds.subreddit_id,
    da.author_id,
    dr.raw_source_file_id,
    df.refined_source_file_id,
    rp.score,
    rp.num_comments,
    rp.upvote_ratio,
    rp.downvote_ratio,
    rp.sentiment,
    rp.intent,

    -- Build proper timestamp from text fields
    TO_TIMESTAMP(
        rp.date_posted || ' ' || rp.time_posted,
        'YYYY-MM-DD HH24:MI:SS'
    ) AS post_created_ts

FROM reddit_posts rp
JOIN dim_subreddit ds
    ON rp.subreddit = ds.subreddit_name
LEFT JOIN dim_author da
    ON rp.author = da.author_name
LEFT JOIN dim_raw_source_file dr
    ON rp.raw_source_file = dr.raw_source_file
LEFT JOIN dim_refined_source_file df
    ON rp.refined_source_file = df.refined_source_file

-- Incremental load protection
ON CONFLICT (post_id) DO NOTHING;