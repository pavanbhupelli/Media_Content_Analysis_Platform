import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import requests
import pandas as pd
from config.config import *

print("Starting YouTube Extraction...")

SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"

search_params = {
    "part": "snippet",
    "q": "music",
    "type": "video",
    "regionCode": REGION_CODE,
    "maxResults": MAX_RESULTS,
    "key": YOUTUBE_API_KEY
}

search_response = requests.get(SEARCH_URL, params=search_params)
print("Search Status Code:", search_response.status_code)

search_json = search_response.json()

if "error" in search_json:
    print("YouTube API Error:", search_json)
    exit()

video_ids = [
    item["id"]["videoId"]
    for item in search_json.get("items", [])
    if "videoId" in item.get("id", {})
]

print("Video IDs Found:", len(video_ids))

if not video_ids:
    print("No videos found. Check API key or quota.")
    exit()

video_params = {
    "part": "snippet,statistics",
    "id": ",".join(video_ids),
    "key": YOUTUBE_API_KEY
}

video_response = requests.get(VIDEO_URL, params=video_params)
print("Video Details Status Code:", video_response.status_code)

video_json = video_response.json()

data = []
for item in video_json.get("items", []):
    data.append({
        "video_id": item["id"],
        "video_title": item["snippet"]["title"],
        "channel_title": item["snippet"]["channelTitle"],
        "category_id": item["snippet"]["categoryId"],
        "view_count": int(item["statistics"].get("viewCount", 0)),
        "like_count": int(item["statistics"].get("likeCount", 0)),
        "comment_count": int(item["statistics"].get("commentCount", 0)),
        "published_at": item["snippet"]["publishedAt"]
    })

df = pd.DataFrame(data)

if df.empty:
    print("DataFrame is empty. Extraction failed.")
else:
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/youtube_raw.csv", index=False)
    print("YouTube Raw File Saved Successfully.")
    print("Rows:", len(df))