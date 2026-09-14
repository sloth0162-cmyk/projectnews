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
    "Accept": (
        "application/rss+xml, application/xml, text/xml, "
        "text/html;q=0.9, */*;q=0.8"
    )
}


def fetch_all_articles(limit_per_source=3):

    articles = []

    print("\n========== RSS FETCH START ==========")
    print(f"🔢 Limit per source: {limit_per_source}")
    print(f"📡 Total RSS sources: {len(RSS_FEEDS)}")

    for feed in RSS_FEEDS:

        source = feed["source"]
        url = feed["url"]

        print("\n----------------------------------------")
        print(f"🌐 START SOURCE: {source}")
        print(f"🔗 URL: {url}")

        try:

            print(f"📡 Sending request to {source}...")

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=(5, 15)
            )

            print(f"✅ Response received from {source}")
            print(f"📡 Status Code: {response.status_code}")
            print(f"📦 Response Size: {len(response.content)} bytes")

            response.raise_for_status()

            print(f"🔍 Parsing RSS for {source}...")

            soup = BeautifulSoup(response.content, "xml")

            items = soup.find_all("item")

            print(f"📰 {source}: Found {len(items)} items")

            if not items:
                print(f"⚠️ {source}: RSS returned 0 items")
                continue

            count = 0

            for item in items[:limit_per_source]:

                if item.title is None or item.link is None:
                    print("⚠️ Skipping item with missing title/link")
                    continue

                title = item.title.get_text(strip=True)
                link = item.link.get_text(strip=True)

                if not title or not link:
                    print("⚠️ Skipping empty title/link")
                    continue

                print(f"➡️ Collected: {title}")

                articles.append({
                    "title": title,
                    "url": link,
                    "source": source
                })

                count += 1

            print(f"✅ {source}: Collected {count} articles")

        except requests.exceptions.Timeout:
            print(f"⏰ TIMEOUT while reading {source}")
            continue

        except requests.exceptions.RequestException as e:
            print(f"❌ REQUEST ERROR while reading {source}")
            print(f"❌ Error: {e}")
            continue

        except Exception as e:
            print(f"❌ UNEXPECTED ERROR while reading {source}")
            print(f"❌ Error: {e}")
            continue

        print(f"🏁 FINISHED SOURCE: {source}")

    print("\n========== RSS FETCH END ==========")
    print(f"✅ Total basic articles collected: {len(articles)}")

    return articles


def scrape_article_content(url):

    print("\n----------------------------------------")
    print("📄 START ARTICLE SCRAPE")
    print(f"🔗 URL: {url}")

    try:

        print("📡 Requesting article page...")

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=(5, 15)
        )

        print("✅ Article response received")
        print(f"📡 Page Status: {response.status_code}")
        print(f"📦 Page Size: {len(response.content)} bytes")

        response.raise_for_status()

        print("🔍 Parsing article HTML...")

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")

        print(f"📝 Found {len(paragraphs)} paragraph elements")

        content = "\n".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
            if p.get_text(strip=True)
        )

        print(f"📝 Extracted {len(content)} characters")

        if not content:
            print("⚠️ Page returned no paragraph content")
            return ""

        print("✅ ARTICLE SCRAPE SUCCESS")

        return content

    except requests.exceptions.Timeout:
        print(f"⏰ TIMEOUT scraping article: {url}")
        return ""

    except requests.exceptions.RequestException as e:
        print(f"❌ REQUEST ERROR scraping article: {url}")
        print(f"❌ Error: {e}")
        return ""

    except Exception as e:
        print(f"❌ UNEXPECTED ERROR scraping article: {url}")
        print(f"❌ Error: {e}")
        return ""


def scrape_news(limit_per_source=3):

    print("\n")
    print("========================================")
    print("🚀 STARTING NEWS SCRAPER")
    print("========================================")

    print("1️⃣ Starting RSS collection...")

    basic_articles = fetch_all_articles(
        limit_per_source=limit_per_source
    )

    print("\n2️⃣ RSS COLLECTION COMPLETE")
    print(f"📊 Received {len(basic_articles)} basic articles")

    if not basic_articles:
        print("⚠️ NO ARTICLES RECEIVED FROM RSS")
        print("🛑 Scraper will return 0 articles")
        return []

    full_articles = []

    print("\n3️⃣ Starting full article scraping...")

    for index, article in enumerate(
        basic_articles,
        start=1
    ):

        print("\n========================================")
        print(
            f"📄 ARTICLE {index}/{len(basic_articles)}"
        )
        print(f"📰 {article['title']}")
        print(f"🌐 Source: {article['source']}")
        print("========================================")

        try:

            content = scrape_article_content(
                article["url"]
            )

            if not content:
                print(
                    f"⚠️ No content found: "
                    f"{article['title']}"
                )
                continue

            full_articles.append({
                "title": article["title"],
                "url": article["url"],
                "source": article["source"],
                "content": content
            })

            print(
                f"✅ FULL ARTICLE ADDED: "
                f"{article['title']}"
            )

        except Exception as e:

            print(
                f"❌ ERROR processing "
                f"'{article['title']}'"
            )

            print(f"❌ Error: {e}")

            continue

    print("\n")
    print("========================================")
    print("🎉 SCRAPER FINISHED")
    print(
        f"🎉 Returning {len(full_articles)} full articles"
    )
    print("========================================")

    return full_articles