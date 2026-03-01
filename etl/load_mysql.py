import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pandas as pd
from sqlalchemy import create_engine
from config.config import *

engine = create_engine(
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
)

yt = pd.read_csv("data/processed/youtube_cleaned.csv")
news = pd.read_csv("data/processed/news_cleaned.csv")

yt.to_sql("youtube_cleaned", engine, if_exists="append", index=False)
news.to_sql("news_cleaned", engine, if_exists="append", index=False)

print("Loaded into MySQL")