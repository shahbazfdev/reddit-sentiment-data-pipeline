INSERT INTO reddit_posts
SELECT *
FROM stg_reddit_posts
ON CONFLICT (id) DO NOTHING;