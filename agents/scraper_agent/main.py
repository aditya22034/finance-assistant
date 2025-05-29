
import requests
import feedparser
from fastapi import FastAPI

app = FastAPI()

@app.get("/scrape_filings")
def get_rss_articles():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get("https://feeds.bbci.co.uk/news/technology/rss.xml", headers=headers)
    feed = feedparser.parse(response.content)

    results = []
    for entry in feed.entries[:5]:
        results.append({
            "title": entry.title,
            "text": entry.summary[:1000] 
        })
    return results
