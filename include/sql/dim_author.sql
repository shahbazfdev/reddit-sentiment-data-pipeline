CREATE TABLE IF NOT EXISTS dim_author (
    author_id SERIAL PRIMARY KEY,
    author_name TEXT UNIQUE
);

INSERT INTO dim_author (author_name)
SELECT DISTINCT author
FROM reddit_posts
WHERE author IS NOT NULL
ON CONFLICT (author_name) DO NOTHING;