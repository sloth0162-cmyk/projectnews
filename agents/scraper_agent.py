import requests
from bs4 import BeautifulSoup

RSS_FEEDS = [
    {"source": "BBC", "url": "https://feeds.bbci.co.uk/news/world/rss.xml"},
    {"source": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml"},
    {"source": "FT", "url": "https://www.ft.com/?format=rss"},
    {"source": "CNBC", "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html"}
]


def fetch_all_articles(limit_per_source=3):
    """Fetch articles from multiple RSS feeds."""
    articles = []

    for feed in RSS_FEEDS:
        print(f"\n🌐 Reading feed: {feed['source']}")

        try:
            response = requests.get(feed["url"], timeout=20)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item")

            print(f"📰 {feed['source']}: Found {len(items)} articles")

            for item in items[:limit_per_source]:
                try:
                    if item.title is None or item.link is None:
                        print("⚠️ Skipping article with missing title/link")
                        continue

                    articles.append({
                        "title": item.title.get_text(strip=True),
                        "url": item.link.get_text(strip=True),
                        "source": feed["source"]
                    })

                except Exception as e:
                    print(f"⚠️ Error parsing article: {e}")

        except Exception as e:
            print(f"❌ Error reading {feed['source']} feed: {e}")

    print(f"\n✅ Total articles collected: {len(articles)}")
    return articles


def scrape_article_content(url):
    """Scrape article content from URL."""
    try:
        print(f"📄 Scraping: {url}")

        response = requests.get(url, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")

        content = "\n".join(
            p.get_text(strip=True)
            for p in paragraphs
            if p.get_text(strip=True)
        )

        print(f"✅ Content length: {len(content)} characters")
        return content

    except Exception as e:
        print(f"❌ Error scraping article: {e}")
        return ""


def scrape_news(limit_per_source=3):
    """Return list of full article data."""
    basic_articles = fetch_all_articles(limit_per_source)
    full_articles = []

    for article in basic_articles:
        try:
            content = scrape_article_content(article["url"])

            full_articles.append({
                "title": article["title"],
                "url": article["url"],
                "source": article["source"],
                "content": content
            })

            print(f"✅ Added: {article['title']}")

        except Exception as e:
            print(f"❌ Error processing article '{article['title']}': {e}")

    print(f"\n🎉 Finished! Returning {len(full_articles)} articles.")
    return full_articles


# Test
if __name__ == "__main__":
    articles = scrape_news(limit_per_source=2)

    for article in articles:
        print("\n==============================")
        print("Source :", article["source"])
        print("Title  :", article["title"])
        print("URL    :", article["url"])
        print("Content:", article["content"][:300], "...")