CREATE TABLE IF NOT EXISTS dim_refined_source_file (
    refined_source_file_id SERIAL PRIMARY KEY,
    refined_source_file TEXT UNIQUE NOT NULL
);

INSERT INTO dim_refined_source_file (refined_source_file)
SELECT DISTINCT refined_source_file
FROM reddit_posts
WHERE refined_source_file IS NOT NULL
ON CONFLICT (refined_source_file) DO NOTHING;