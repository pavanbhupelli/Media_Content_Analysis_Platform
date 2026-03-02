# 📊 Media Content Analysis Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![BigQuery](https://img.shields.io/badge/Google-BigQuery-orange)
![MySQL](https://img.shields.io/badge/Database-MySQL-blue)
![Architecture](https://img.shields.io/badge/Data%20Model-Star%20Schema-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

---

## 📌 Project Overview

The **Media Content Analysis Platform** is an end-to-end Data Engineering project designed to extract, transform, and analyze media content data from:

- 🎥 YouTube Data API  
- 📰 News JSON Dataset  

The system processes raw data, performs cleaning and feature engineering, loads it into **Google BigQuery** and **MySQL**, and builds a **Star Schema Data Warehouse** to generate analytical insights such as:

- Top performing videos  
- Channel performance metrics  
- Engagement analysis  

---

# 🏗️ Architecture Overview

The project follows a **Layered ETL Architecture** combined with a **Star Schema Data Warehouse Model**.

---

## 🔄 Data Flow Architecture

```
YouTube API + News Dataset
        ↓
Extraction Layer
        ↓
Raw Data Storage
        ↓
Transformation Layer
        ↓
Processed Data
        ↓
Loading Layer
        ↓
BigQuery & MySQL
        ↓
Staging Tables
        ↓
Dimension Tables
        ↓
Fact Table
        ↓
Data Marts
        ↓
Analytics & Insights
```

---

# 📂 Project Structure

```
MEDIA-CONTENT-ANALYSIS-PLATFORM
│
├── config/                     # Configuration Layer
│   ├── config.py               # API keys & DB configs
│   └── gcp_credentials.json    # GCP authentication
│
├── data/                       # Data Storage Layer
│   ├── raw/                    # Raw extracted data
│   │   ├── news_raw.json
│   │   ├── youtube_raw.csv
│   │   └── news_category.json
│   │
│   └── processed/              # Cleaned & transformed data
│       ├── news_cleaned.csv
│       └── youtube_cleaned.csv
│
├── etl/                        # ETL Layer
│   ├── extract_news.py
│   ├── extract_youtube.py
│   ├── transform_news.py
│   ├── transform_youtube.py
│   ├── load_bigquery.py
│   └── load_mysql.py
│
├── warehouse/                  # Data Warehouse Layer
│   ├── staging.sql
│   ├── dimension_tables.sql
│   ├── fact_tables.sql
│   └── data_marts.sql
│
├── run_pipeline.py             # Pipeline Orchestration
├── requirements.txt            # Dependencies
├── .gitignore                  # Security control
└── README.md                   # Documentation
```

---

# 🔹 ETL Process

## 1️⃣ Extraction Layer

**Files:**
- `extract_youtube.py`
- `extract_news.py`

**Responsibilities:**
- Fetch video metadata and statistics using YouTube API
- Read news dataset from JSON
- Store raw data in `data/raw/`

---

## 2️⃣ Transformation Layer

**Files:**
- `transform_youtube.py`
- `transform_news.py`

**Operations Performed:**
- Remove unwanted characters
- Convert date formats
- Handle null values
- Feature engineering

### Engagement Score Calculation

```python
engagement_score = (like_count + comment_count) / view_count
```

---

## 3️⃣ Loading Layer

**Files:**
- `load_bigquery.py`
- `load_mysql.py`

**Responsibilities:**
- Load processed CSV files into:
  - Google BigQuery (staging tables)
  - MySQL database

---

# 🏢 Data Warehouse Design (Star Schema)

## ⭐ Staging Tables

- `stg_youtube`
- `stg_news`

---

## ⭐ Dimension Tables

### `dim_channel`

- channel_id (Primary Key)  
- channel_title  

### `dim_category`

- category_id (Primary Key)  
- category_name  

---

## ⭐ Fact Table

### `fact_youtube`

- video_id (Primary Key)  
- channel_id (Foreign Key)  
- category_id (Foreign Key)  
- published_date  
- view_count  
- like_count  
- comment_count  
- engagement_score  

**Grain:** One row per video.

---

# ⭐ Star Schema Model

```
              dim_channel
                   |
                   |
dim_category ---- fact_youtube
```

✔ Central measurable table  
✔ Surrounding descriptive dimensions  
✔ Optimized for analytical queries  

---

# 📊 Data Marts

- `mart_top_videos` → Top 10 videos by views  
- `mart_channel_performance` → Channel-level aggregated performance  

---

# 🛠️ Tech Stack

- Python  
- Pandas  
- YouTube Data API  
- Google BigQuery  
- MySQL  
- SQL  
- Git & GitHub  

---

# 🔐 Security & Best Practices

- Credentials excluded via `.gitignore`
- No hardcoded secrets
- Layered ETL design
- Star schema modeling
- Clean modular architecture

---

# 🚀 How to Run the Project

## 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 2️⃣ Configure Environment

Add:
- YouTube API Key
- MySQL credentials
- GCP credentials file

## 3️⃣ Run the Pipeline

```bash
python run_pipeline.py
```

---

# 🎯 Key Highlights

- End-to-end ETL pipeline  
- Feature engineering (Engagement Score)  
- Star Schema Data Warehouse  
- Cloud + relational database integration  
- Production-ready structure  

---
