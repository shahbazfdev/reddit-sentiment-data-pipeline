CREATE TABLE IF NOT EXISTS reddit_posts (
    id TEXT PRIMARY KEY,
    subreddit TEXT,
    title TEXT,
    author TEXT,
    score INT,
    num_comments INT,
    upvote_ratio FLOAT,
    downvote_ratio FLOAT,
    url TEXT,
    sentiment TEXT,
    intent TEXT,
    date_posted TEXT,
    time_posted TEXT,
    date_added TEXT NOT NULL,
    time_added TEXT NOT NULL,
    raw_source_file TEXT,
    refined_source_file TEXT
);
