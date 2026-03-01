CREATE OR REPLACE TABLE media_warehouse.dim_channel AS
SELECT DISTINCT channel_title
FROM media_warehouse.stg_youtube;

CREATE OR REPLACE TABLE media_warehouse.dim_category AS
SELECT DISTINCT category_id
FROM media_warehouse.stg_youtube;