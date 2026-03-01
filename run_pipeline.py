import subprocess
import sys

def run(script):
    subprocess.run([sys.executable, script], check=True)

run("etl/extract_youtube.py")
run("etl/extract_news.py")
run("etl/transform_youtube.py")
run("etl/transform_news.py")
run("etl/load_mysql.py")
run("etl/load_bigquery.py")

print("Pipeline Completed Successfully")