import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import csv

print("Transforming News Data...")

df = pd.read_json("data/raw/news_raw.json", lines=True)

df = df[["category", "headline", "short_description", "date"]]

# Clean text fields
df["headline"] = (
    df["headline"]
    .astype(str)
    .str.replace("\n", " ")
    .str.replace("\r", " ")
)

df["short_description"] = (
    df["short_description"]
    .astype(str)
    .str.replace("\n", " ")
    .str.replace("\r", " ")
)

df["date"] = pd.to_datetime(df["date"], errors="coerce")

df = df.dropna()

os.makedirs("data/processed", exist_ok=True)

# 🔥 IMPORTANT: Proper CSV formatting
df.to_csv(
    "data/processed/news_cleaned.csv",
    index=False,
    quoting=csv.QUOTE_ALL,      # Quote everything
    escapechar="\\"
)

print("News Transformed Successfully")
print("Rows:", len(df))