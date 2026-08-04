import requests
from bs4 import BeautifulSoup

RSS_FEEDS = [
    {"source": "BBC", "url": "https://feeds.bbci.co.uk/news/world/rss.xml"},
    {"source": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml"},
    {"source": "FT", "url": "https://www.ft.com/?format=rss"},
    {"source": "CNBC", "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html"}
]
def fetch_all_articles(limit_per_source=3):
    articles = []

    for feed in RSS_FEEDS:
        print(f"\n🌐 Reading feed: {feed['source']}")

        try:
            response = requests.get(feed["url"], timeout=20)
            print(f"Status: {response.status_code}")

            response.raise_for_status()

            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item")

            print(f"📰 {feed['source']}: Found {len(items)} items")

            for item in items[:limit_per_source]:
                print("TITLE:", item.title)
                print("LINK :", item.link)

                if item.title is None or item.link is None:
                    print("⚠️ Missing title/link")
                    continue

                articles.append({
                    "title": item.title.get_text(strip=True),
                    "url": item.link.get_text(strip=True),
                    "source": feed["source"]
                })

        except Exception as e:
            print(f"❌ Error reading {feed['source']}: {e}")

    print(f"✅ Total articles collected: {len(articles)}")
    return articles