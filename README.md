Media Content Analysis Platform

PROJECT ARCHITECTURE (Exact Folder-Based Structure)

MEDIA-CONTENT-ANALYSIS-PLATFORM
│
├── config/                     → Configuration Layer
│   ├── __init__.py
│   ├── config.py               → API keys, DB configs
│   └── gcp_credentials.json    → GCP authentication
│
├── data/                       → Data Storage Layer
│   ├── raw/                    → Raw extracted data
│   │   ├── news_raw.json
│   │   ├── youtube_raw.csv
│   │   └── news_category.json
│   │
│   └── processed/              → Cleaned & transformed data
│       ├── news_cleaned.csv
│       └── youtube_cleaned.csv
│
├── etl/                        → ETL Layer
│   ├── extract_news.py
│   ├── extract_youtube.py
│   ├── transform_news.py
│   ├── transform_youtube.py
│   ├── load_bigquery.py
│   └── load_mysql.py
│
├── warehouse/                  → Data Warehouse Layer
│   ├── staging.sql
│   ├── dimension_tables.sql
│   ├── fact_tables.sql
│   └── data_marts.sql
│
├── run_pipeline.py             → Pipeline Orchestration
├── requirements.txt            → Dependencies
├── .gitignore                  → Security control
└── README.md                   → Documentation

OVERALL ARCHITECTURE FLOW (STEP-BY-STEP)
YouTube API + News Dataset
        ↓
Extraction (etl/)
        ↓
Raw Data (data/raw)
        ↓
Transformation (etl/)
        ↓
Processed Data (data/processed)
        ↓
Loading (BigQuery + MySQL)
        ↓
Staging Tables
        ↓
Dimension Tables
        ↓
Fact Table
        ↓
Data Marts
        ↓
Analytics / Insights


Step 1: Configuration Layer (config/)

Stores API keys and database credentials.

Used for connecting to:

YouTube API

Google BigQuery

MySQL

Step 2: Extraction Layer (etl/extract_*.py)
Files:

extract_youtube.py

extract_news.py

What Happens:

Calls YouTube API using requests

Reads News JSON dataset

Stores raw data inside:

Step 3: Transformation Layer (etl/transform_*.py)
Files:

transform_youtube.py

transform_news.py

Operations Performed:

Remove unwanted characters

Convert date formats

Drop null values

Create new feature:

Step 4: Loading Layer (etl/load_*.py)
Files:

load_bigquery.py

load_mysql.py

What Happens:

Load cleaned CSV into:

BigQuery staging tables

MySQL tables

DATA WAREHOUSE ARCHITECTURE (warehouse/)
1Staging Layer (staging.sql)

Tables:

stg_youtube
stg_news

Dimension Tables (dimension_tables.sql)
dim_channel
dim_category

dim_channel
 ├── channel_id (PK)
 └── channel_title

dim_category
 ├── category_id (PK)
 └── category_name

 Fact Table (fact_tables.sql)
 fact_youtube
 ├── video_id (PK)
 ├── channel_id (FK)
 ├── category_id (FK)
 ├── published_date
 ├── view_count
 ├── like_count
 ├── comment_count
 └── engagement_score

 Data Marts (data_marts.sql)
 mart_top_videos
mart_channel_performance

STAR SCHEMA (Final Model)
              dim_channel
                   |
                   |
dim_category ---- fact_youtube
