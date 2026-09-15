import feedparser
import requests
from bs4 import BeautifulSoup


RSS_FEEDS = [
    {
        "source": "BBC",
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
    },
    {
        "source": "Al Jazeera",
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
    },
    {
        "source": "FT",
        "url": "https://www.ft.com/?format=rss",
    },
    {
        "source": "CNBC",
        "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    },
]

MAX_ARTICLES = 4

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}


def clean_text(value):
    if not value:
        return ""

    soup = BeautifulSoup(value, "html.parser")
    return " ".join(
        soup.get_text(" ", strip=True).split()
    )


def extract_content(entry):
    # Full RSS/Atom content
    if getattr(entry, "content", None):
        for block in entry.content:
            text = clean_text(block.get("value", ""))
            if text:
                return text

    # RSS summary
    summary = clean_text(
        getattr(entry, "summary", "")
    )

    if summary:
        return summary

    # RSS description
    return clean_text(
        getattr(entry, "description", "")
    )


def fetch_feed(feed):
    source = feed["source"]
    url = feed["url"]

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
        )

        response.raise_for_status()

        parsed = feedparser.parse(response.content)

        if not parsed.entries:
            return [], f"{source}: RSS returned no items"

        return parsed.entries, None

    except requests.exceptions.Timeout:
        return [], f"{source}: request timed out"

    except Exception as e:
        return [], f"{source}: {type(e).__name__}: {e}"


def scrape_news():
    print("\n🚀 NEWS SCRAPER STARTED")

    articles = []
    errors = []

    for feed in RSS_FEEDS:

        if len(articles) >= MAX_ARTICLES:
            break

        source = feed["source"]

        entries, error = fetch_feed(feed)

        if error:
            errors.append(error)
            print(f"❌ {error}")
            continue

        found = False

        for entry in entries:

            title = clean_text(
                getattr(entry, "title", "")
            )

            link = getattr(entry, "link", "").strip()

            content = extract_content(entry)

            if not title:
                continue

            if not link:
                continue

            if not content:
                print(
                    f"⚠️ {source}: no content — {title}"
                )
                continue

            articles.append({
                "title": title,
                "url": link,
                "source": source,
                "content": content,
            })

            print(
                f"✅ Added: {source} - {title}"
            )

            found = True
            break

        if not found:
            error = f"{source}: no usable article found"
            errors.append(error)
            print(f"⚠️ {error}")

    scrape_news.last_errors = errors

    print(
        f"📊 Scraper finished — "
        f"{len(articles)} articles, "
        f"{len(errors)} errors"
    )

    for error in errors:
        print(f"   - {error}")

    if not articles:
        raise RuntimeError(
            "No usable articles from any feed. "
            f"Errors: {errors}"
        )

    return articles[:MAX_ARTICLES]


scrape_news.last_errors = []