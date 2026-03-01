import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pandas as pd

df = pd.read_csv("data/raw/youtube_raw.csv")

df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
df = df.dropna()

df["engagement_score"] = (
    (df["like_count"] + df["comment_count"]) / df["view_count"]
)

df.to_csv("data/processed/youtube_cleaned.csv", index=False)

print("YouTube Transformed")