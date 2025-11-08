import requests
import os
from services.llm_utils import generate_summary
from services.supabase_client import save_summary_to_db

RSS_FEEDS = [
    "https://www.reuters.com/rssFeed/businessNews",
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"
]

def fetch_articles():
    articles = []
    for feed in RSS_FEEDS:
        try:
            response = requests.get(feed)
            if response.status_code == 200:
                # Parse RSS feed (basic, can add XML parsing later)
                articles.append({"title": "Sample Article", "content": "Sample content from feed"})
        except Exception as e:
            print("Error fetching feed:", e)
    return articles

# agents/summarizer_agent.py

from services.llm_utils import generate_summary


def summarize_text(content: str):
    """Summarize a single article using the LLM."""
    return generate_summary(content)
