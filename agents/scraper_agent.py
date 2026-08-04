import requests
from bs4 import BeautifulSoup

RSS_FEEDS = [
    {"source": "BBC", "url": "https://feeds.bbci.co.uk/news/world/rss.xml"},
    {"source": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml"},
    {"source": "FT", "url": "https://www.ft.com/?format=rss"},
    {"source": "CNBC", "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html"}
]


def fetch_all_articles(limit_per_source=3):
    """Fetch article titles and URLs from RSS feeds."""
    articles = []

    for feed in RSS_FEEDS:
        print(f"\n🌐 Reading feed: {feed['source']}")

        try:
            response = requests.get(
                feed["url"],
                timeout=20,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            print(f"Status Code: {response.status_code}")

            response.raise_for_status()

            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item")

            print(f"📰 {feed['source']}: Found {len(items)} items")

            for item in items[:limit_per_source]:

                if item.title is None or item.link is None:
                    print("⚠️ Skipping item with missing title/link")
                    continue

                title = item.title.get_text(strip=True)
                link = item.link.get_text(strip=True)

                print(f"➡️ {title}")

                articles.append({
                    "title": title,
                    "url": link,
                    "source": feed["source"]
                })

        except Exception as e:
            print(f"❌ Error reading {feed['source']} feed: {e}")

    print(f"\n✅ Total articles collected: {len(articles)}")
    return articles


def scrape_article_content(url):
    """Scrape article body from webpage."""

    print(f"\n📄 Scraping: {url}")

    try:
        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        print(f"Page Status: {response.status_code}")

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")

        content = "\n".join(
            p.get_text(strip=True)
            for p in paragraphs
            if p.get_text(strip=True)
        )

        print(f"✅ Extracted {len(content)} characters")

        return content

    except Exception as e:
        print(f"❌ Error scraping article: {e}")
        return ""


def scrape_news(limit_per_source=3):
    """Return full article data."""

    print("🚀 Starting scraper...")

    basic_articles = fetch_all_articles(limit_per_source)

    full_articles = []

    for article in basic_articles:

        try:
            content = scrape_article_content(article["url"])

            if not content:
                print(f"⚠️ No content found for: {article['title']}")
                continue

            full_articles.append({
                "title": article["title"],
                "url": article["url"],
                "source": article["source"],
                "content": content
            })

            print(f"✅ Added: {article['title']}")

        except Exception as e:
            print(f"❌ Error processing article '{article['title']}': {e}")

    print(f"\n🎉 Returning {len(full_articles)} articles.")

    return full_articles


if __name__ == "__main__":
    articles = scrape_news(limit_per_source=2)

    print(f"\nReturned {len(articles)} articles.\n")

    for article in articles:
        print("=" * 60)
        print("Source :", article["source"])
        print("Title  :", article["title"])
        print("URL    :", article["url"])
        print("Content:", article["content"][:300], "...")