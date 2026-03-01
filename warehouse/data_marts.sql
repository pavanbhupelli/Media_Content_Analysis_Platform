CREATE OR REPLACE TABLE media_warehouse.mart_top_videos AS
SELECT
video_title,
channel_title,
view_count
FROM media_warehouse.fact_youtube
ORDER BY view_count DESC
LIMIT 10;

CREATE OR REPLACE TABLE media_warehouse.mart_channel_performance AS
SELECT
channel_title,
SUM(view_count) AS total_views
FROM media_warehouse.fact_youtube
GROUP BY channel_title;