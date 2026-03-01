import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from google.cloud import bigquery
from google.oauth2 import service_account
from config.config import *

# Load credentials manually
credentials = service_account.Credentials.from_service_account_file(
    "config/gcp_credentials.json"
)

client = bigquery.Client(
    credentials=credentials,
    project=PROJECT_ID
)

dataset_id = f"{PROJECT_ID}.{DATASET}"

def load_csv(table_name, file_path):
    table_id = f"{dataset_id}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition="WRITE_TRUNCATE",
    )

    with open(file_path, "rb") as f:
        job = client.load_table_from_file(f, table_id, job_config=job_config)

    job.result()
    print(f"{table_name} loaded successfully")

load_csv("stg_youtube", "data/processed/youtube_cleaned.csv")
load_csv("stg_news", "data/processed/news_cleaned.csv")