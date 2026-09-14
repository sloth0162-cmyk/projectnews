import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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

MAX_ARTICLES = 4


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "application/rss+xml, application/xml, text/xml, "
        "text/html;q=0.9, */*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}


def create_session():

    session = requests.Session()

    retry = Retry(
        total=2,
        connect=2,
        read=2,
        status=2,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False
    )

    adapter = HTTPAdapter(max_retries=retry)

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    session.headers.update(HEADERS)

    return session


session = create_session()


def clean_text(value):

    if not value:
        return ""

    soup = BeautifulSoup(value, "html.parser")

    return " ".join(
        soup.get_text(" ", strip=True).split()
    )


def extract_rss_content(item):

    description = item.find("description")

    if description:
        text = clean_text(description.get_text())

        if text:
            return text

    for tag in item.find_all():

        name = str(tag.name).lower()

        if name in ("encoded", "summary", "content"):

            text = clean_text(tag.get_text())

            if text:
                return text

    return ""


def scrape_article_content(url):

    try:

        response = session.get(
            url,
            timeout=(10, 15),
            allow_redirects=True
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Try article containers first
        for selector in [
            "article",
            "[class*='article-body']",
            "[class*='article-content']",
            "[class*='story-body']",
            "[class*='story-content']",
            "main"
        ]:

            for element in soup.select(selector):

                text = element.get_text(
                    " ",
                    strip=True
                )

                text = " ".join(text.split())

                if len(text) >= 300:
                    return text

        # Paragraph fallback
        paragraphs = []

        for p in soup.find_all("p"):

            text = " ".join(
                p.get_text(" ", strip=True).split()
            )

            if len(text) >= 30:
                paragraphs.append(text)

        content = " ".join(paragraphs)

        if len(content) >= 300:
            return content

        return ""

    except Exception as e:

        print(
            f"⚠️ Article scrape failed: "
            f"{type(e).__name__}: {e}"
        )

        return ""


def fetch_all_articles(errors):

    articles = []

    for feed in RSS_FEEDS:

        if len(articles) >= MAX_ARTICLES:
            break

        source = feed["source"]
        url = feed["url"]

        print(f"\n🌐 Checking {source}")

        try:

            response = session.get(
                url,
                timeout=(10, 15),
                allow_redirects=True
            )

            print(
                f"📡 {source}: "
                f"HTTP {response.status_code}"
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.content,
                "xml"
            )

            items = soup.find_all("item")

            if not items:
                message = f"{source}: RSS returned no items"
                print(f"⚠️ {message}")
                errors.append(message)
                continue

            # Take the newest usable item from this feed
            for item in items:

                if len(articles) >= MAX_ARTICLES:
                    break

                title_tag = item.find("title")
                link_tag = item.find("link")

                if not title_tag or not link_tag:
                    continue

                title = clean_text(
                    title_tag.get_text()
                )

                link = link_tag.get_text(
                    strip=True
                )

                if not link:
                    link = link_tag.get("href", "").strip()

                if not title or not link:
                    continue

                rss_content = extract_rss_content(item)

                # Prefer RSS content
                content = rss_content

                # Fallback to article page
                if len(content) < 300:

                    print(
                        f"🌐 RSS content weak for: {title}"
                    )

                    content = scrape_article_content(
                        link
                    )

                if not content:

                    print(
                        f"⚠️ No usable content: {title}"
                    )

                    continue

                articles.append({
                    "title": title,
                    "url": link,
                    "source": source,
                    "content": content
                })

                print(
                    f"✅ Added: {source} - {title}"
                )

                # One article per feed is enough
                break

        except Exception as e:

            message = (
                f"{source}: "
                f"{type(e).__name__}: {e}"
            )

            print(f"❌ {message}")
            errors.append(message)

    return articles


def scrape_news():

    print("\n========================================")
    print("🚀 NEWS SCRAPER STARTED")
    print("========================================")

    errors = []

    articles = fetch_all_articles(errors)

    # Store errors so run_pipeline can report them
    scrape_news.last_errors = errors

    print("\n========================================")
    print("📊 SCRAPER RESULT")
    print("========================================")
    print(f"📰 Articles: {len(articles)}")
    print(f"⚠️ Feed errors: {len(errors)}")

    for error in errors:
        print(f"   - {error}")

    # Minimum = 1 article
    if not articles:

        message = (
            "Scraper failed: no usable articles "
            "were returned from any feed."
        )

        print(f"❌ {message}")

        raise RuntimeError(message)

    # Maximum = 4 articles
    articles = articles[:MAX_ARTICLES]

    print(
        f"✅ Returning {len(articles)} articles"
    )

    print("========================================")

    return articles


# Used by run_pipeline
scrape_news.last_errors = []