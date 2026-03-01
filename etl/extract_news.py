import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import shutil

shutil.copy("data/news_category.json", "data/raw/news_raw.json")

print("News Raw Copied")