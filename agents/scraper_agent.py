import requests
from bs4 import BeautifulSoup


RSS_FEEDS = [
    {
        "source": "BBC",
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml"
    },
    {
        "source": "Al Jazeera",
        "url": "https://www.aljazeera.com/xml/rss/all.xml"
    },
    {
        "source": "FT",
        "url": "https://www.ft.com/?format=rss"
    },
    {
        "source": "CNBC",
        "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html"
    }
]


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/xml, text/html;q=0.9, */*;q=0.8"
}


def fetch_all_articles(limit_per_source=3):
    """Fetch article titles and URLs from RSS feeds."""

    articles = []

    print("\n========== RSS FETCH START ==========")

    for feed in RSS_FEEDS:

        source = feed["source"]
        url = feed["url"]

        print(f"\n🌐 Reading feed: {source}")
        print(f"🔗 URL: {url}")

        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=(5, 15)
            )

            print(f"📡 Status Code: {response.status_code}")
            print(f"📦 Response Size: {len(response.content)} bytes")

            response.raise_for_status()

            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item")

            print(f"📰 {source}: Found {len(items)} items")

            if not items:
                print(f"⚠️ {source}: RSS returned 0 items")
                continue

            for item in items[:limit_per_source]:

                if item.title is None or item.link is None:
                    print("⚠️ Skipping item with missing title/link")
                    continue

                title = item.title.get_text(strip=True)
                link = item.link.get_text(strip=True)

                if not title or not link:
                    print("⚠️ Skipping empty title/link")
                    continue

                print(f"➡️ {title}")

                articles.append({
                    "title": title,
                    "url": link,
                    "source": source
                })

        except requests.exceptions.Timeout:
            print(f"⏰ TIMEOUT while reading {source}")

        except requests.exceptions.RequestException as e:
            print(f"❌ REQUEST ERROR while reading {source}: {e}")

        except Exception as e:
            print(f"❌ UNEXPECTED ERROR while reading {source}: {e}")

    print("\n========== RSS FETCH END ==========")
    print(f"✅ Total basic articles collected: {len(articles)}")

    return articles


def scrape_article_content(url):
    """Scrape article body from webpage."""

    print(f"\n📄 Scraping article:")
    print(f"🔗 {url}")

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=(5, 15)
        )

        print(f"📡 Page Status: {response.status_code}")
        print(f"📦 Page Size: {len(response.content)} bytes")

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")

        content = "\n".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
            if p.get_text(strip=True)
        )

        print(f"📝 Extracted {len(content)} characters")

        if not content:
            print("⚠️ Page returned no paragraph content")
            return ""

        return content

    except requests.exceptions.Timeout:
        print(f"⏰ TIMEOUT scraping article: {url}")
        return ""

    except requests.exceptions.RequestException as e:
        print(f"❌ REQUEST ERROR scraping article: {e}")
        return ""

    except Exception as e:
        print(f"❌ UNEXPECTED ERROR scraping article: {e}")
        return ""


def scrape_news(limit_per_source=3):
    """Fetch RSS articles and scrape their full content."""

    print("\n========================================")
    print("🚀 STARTING NEWS SCRAPER")
    print("========================================")

    basic_articles = fetch_all_articles(
        limit_per_source=limit_per_source
    )

    print(
        f"\n📊 RSS stage complete. "
        f"Received {len(basic_articles)} articles."
    )

    full_articles = []

    for index, article in enumerate(basic_articles, start=1):

        print(
            f"\n========== ARTICLE {index}/{len(basic_articles)} =========="
        )

        try:
            content = scrape_article_content(article["url"])

            if not content:
                print(
                    f"⚠️ No content found for: "
                    f"{article['title']}"
                )
                continue

            full_articles.append({
                "title": article["title"],
                "url": article["url"],
                "source": article["source"],
                "content": content
            })

            print(f"✅ Added: {article['title']}")

        except Exception as e:
            print(
                f"❌ ERROR processing "
                f"'{article['title']}': {e}"
            )

    print("\n========================================")
    print(f"🎉 SCRAPER FINISHED")
    print(f"🎉 Returning {len(full_articles)} full articles")
    print("========================================\n")

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