CREATE TABLE IF NOT EXISTS dim_raw_source_file (
    raw_source_file_id SERIAL PRIMARY KEY,
    raw_source_file TEXT UNIQUE NOT NULL
);

INSERT INTO dim_raw_source_file (raw_source_file)
SELECT DISTINCT raw_source_file
FROM reddit_posts
WHERE raw_source_file IS NOT NULL
ON CONFLICT (raw_source_file) DO NOTHING;