import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# =========================================================
# RSS SOURCES
# =========================================================

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


# =========================================================
# REQUEST SESSION
# =========================================================

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
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}


def create_session():

    session = requests.Session()

    retry_strategy = Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )

    adapter = HTTPAdapter(
        max_retries=retry_strategy
    )

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    session.headers.update(HEADERS)

    return session


session = create_session()


# =========================================================
# CLEAN HTML / TEXT
# =========================================================

def clean_text(value):

    if not value:
        return ""

    soup = BeautifulSoup(
        value,
        "html.parser"
    )

    text = soup.get_text(
        " ",
        strip=True
    )

    return " ".join(text.split())


# =========================================================
# EXTRACT RSS DESCRIPTION
# =========================================================

def extract_rss_content(item):

    # Standard RSS
    description = item.find("description")

    if description:
        text = clean_text(
            description.get_text()
        )

        if text:
            return text

    # Some feeds may expose content differently
    content_encoded = item.find(
        "content:encoded"
    )

    if content_encoded:
        text = clean_text(
            content_encoded.get_text()
        )

        if text:
            return text

    # Fallback for namespace parsing
    for tag in item.find_all():

        if tag.name and (
            str(tag.name).lower()
            in [
                "encoded",
                "summary",
                "content"
            ]
        ):

            text = clean_text(
                tag.get_text()
            )

            if text:
                return text

    return ""


# =========================================================
# FETCH RSS FEEDS
# =========================================================

def fetch_all_articles(limit_per_source=3):

    articles = []

    print("\n========================================")
    print("🚀 RSS COLLECTION START")
    print("========================================")

    print(f"🔢 Limit per source: {limit_per_source}")
    print(f"📡 Sources: {len(RSS_FEEDS)}")

    for feed in RSS_FEEDS:

        source = feed["source"]
        url = feed["url"]

        print("\n----------------------------------------")
        print(f"🌐 SOURCE: {source}")
        print(f"🔗 URL: {url}")

        try:

            print("📡 Requesting RSS...")

            response = session.get(
                url,
                timeout=(10, 20),
                allow_redirects=True
            )

            print("✅ RSS RESPONSE RECEIVED")
            print(f"📡 Status: {response.status_code}")
            print(f"🔗 Final URL: {response.url}")
            print(f"📦 Size: {len(response.content)} bytes")

            response.raise_for_status()

            print("🔍 Parsing RSS...")

            soup = BeautifulSoup(
                response.content,
                "xml"
            )

            items = soup.find_all("item")

            print(
                f"📰 {source}: "
                f"{len(items)} RSS items found"
            )

            if not items:

                print(
                    f"⚠️ {source}: "
                    f"No RSS items found"
                )

                continue

            collected = 0

            for item in items:

                if collected >= limit_per_source:
                    break

                # -----------------------------------------
                # TITLE
                # -----------------------------------------

                title_tag = item.find("title")

                if not title_tag:

                    print(
                        "⚠️ Missing title - skipping"
                    )

                    continue

                title = clean_text(
                    title_tag.get_text()
                )

                # -----------------------------------------
                # LINK
                # -----------------------------------------

                link_tag = item.find("link")

                if not link_tag:

                    print(
                        "⚠️ Missing link - skipping"
                    )

                    continue

                link = link_tag.get_text(
                    strip=True
                )

                # Some RSS feeds can store URL
                # differently
                if not link:

                    href = link_tag.get(
                        "href"
                    )

                    if href:
                        link = href.strip()

                if not title or not link:

                    print(
                        "⚠️ Empty title/link - skipping"
                    )

                    continue

                # -----------------------------------------
                # DESCRIPTION
                # -----------------------------------------

                rss_content = extract_rss_content(
                    item
                )

                print(f"\n➡️ TITLE: {title}")
                print(f"🔗 LINK: {link}")
                print(
                    f"📝 RSS CONTENT: "
                    f"{len(rss_content)} chars"
                )

                if rss_content:

                    print(
                        "✅ RSS already contains "
                        "article content/summary"
                    )

                else:

                    print(
                        "⚠️ RSS has no usable description"
                    )

                articles.append(
                    {
                        "title": title,
                        "url": link,
                        "source": source,
                        "rss_content": rss_content,
                    }
                )

                collected += 1

            print(
                f"\n✅ {source}: "
                f"Collected {collected}"
            )

        except requests.exceptions.Timeout:

            print(
                f"⏰ TIMEOUT: {source}"
            )
            continue

        except requests.exceptions.RequestException as e:

            print(
                f"❌ REQUEST ERROR: {source}"
            )
            print(
                f"❌ {type(e).__name__}: {e}"
            )
            continue

        except Exception as e:

            print(
                f"❌ RSS PARSING ERROR: {source}"
            )
            print(
                f"❌ {type(e).__name__}: {e}"
            )
            continue

    print("\n========================================")
    print("✅ RSS COLLECTION FINISHED")
    print(
        f"📰 Total articles: {len(articles)}"
    )
    print("========================================")

    return articles


# =========================================================
# WEBPAGE ARTICLE SCRAPER
# =========================================================

def scrape_article_content(url):

    print("\n----------------------------------------")
    print("📄 WEBPAGE SCRAPE START")
    print(f"🔗 {url}")

    try:

        response = session.get(
            url,
            timeout=(10, 20),
            allow_redirects=True
        )

        print(
            f"📡 Status: {response.status_code}"
        )

        print(
            f"🔗 Final URL: {response.url}"
        )

        print(
            f"📦 Size: {len(response.content)} bytes"
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # -----------------------------------------
        # Try likely article containers first
        # -----------------------------------------

        selectors = [

            "article",

            "[class*='article-body']",
            "[class*='article-content']",

            "[class*='story-body']",
            "[class*='story-content']",

            "[class*='post-content']",

            "main"
        ]

        for selector in selectors:

            elements = soup.select(
                selector
            )

            for element in elements:

                text = element.get_text(
                    "\n",
                    strip=True
                )

                text = "\n".join(
                    line.strip()
                    for line in text.splitlines()
                    if line.strip()
                )

                if len(text) >= 500:

                    print(
                        f"✅ ARTICLE FOUND USING: "
                        f"{selector}"
                    )

                    print(
                        f"📝 Characters: "
                        f"{len(text)}"
                    )

                    return text

        # -----------------------------------------
        # Generic paragraph fallback
        # -----------------------------------------

        print(
            "🔍 Article container not found."
        )

        print(
            "🔍 Trying paragraph extraction..."
        )

        paragraphs = soup.find_all("p")

        useful_paragraphs = []

        for paragraph in paragraphs:

            text = paragraph.get_text(
                " ",
                strip=True
            )

            text = " ".join(
                text.split()
            )

            if len(text) >= 30:

                useful_paragraphs.append(
                    text
                )

        content = "\n".join(
            useful_paragraphs
        )

        print(
            f"📝 Paragraphs found: "
            f"{len(useful_paragraphs)}"
        )

        print(
            f"📝 Extracted characters: "
            f"{len(content)}"
        )

        if len(content) >= 500:

            print(
                "✅ ARTICLE SCRAPE SUCCESS"
            )

            return content

        print(
            "⚠️ WEBPAGE DOES NOT CONTAIN "
            "ENOUGH ARTICLE TEXT"
        )

        return ""

    except requests.exceptions.Timeout:

        print(
            f"⏰ ARTICLE TIMEOUT: {url}"
        )

        return ""

    except requests.exceptions.RequestException as e:

        print(
            f"❌ ARTICLE REQUEST ERROR: {url}"
        )

        print(
            f"❌ {type(e).__name__}: {e}"
        )

        return ""

    except Exception as e:

        print(
            f"❌ ARTICLE SCRAPE ERROR: {url}"
        )

        print(
            f"❌ {type(e).__name__}: {e}"
        )

        return ""


# =========================================================
# MAIN NEWS SCRAPER
# =========================================================

def scrape_news(limit_per_source=3):

    print("\n")
    print("========================================")
    print("🚀 STARTING NEWS SCRAPER")
    print("========================================")

    # =====================================================
    # STEP 1 — RSS
    # =====================================================

    print("\n1️⃣ STEP 1: RSS COLLECTION")

    basic_articles = fetch_all_articles(
        limit_per_source=limit_per_source
    )

    print("\n----------------------------------------")
    print(
        f"📊 RSS returned "
        f"{len(basic_articles)} articles"
    )
    print("----------------------------------------")

    if not basic_articles:

        print(
            "❌ NO RSS ARTICLES RECEIVED"
        )

        return []

    # =====================================================
    # STEP 2 — BUILD FULL ARTICLES
    # =====================================================

    print("\n2️⃣ STEP 2: BUILDING ARTICLE CONTENT")

    full_articles = []

    for index, article in enumerate(
        basic_articles,
        start=1
    ):

        title = article["title"]
        url = article["url"]
        source = article["source"]
        rss_content = article.get(
            "rss_content",
            ""
        )

        print("\n========================================")
        print(
            f"📄 ARTICLE {index}/"
            f"{len(basic_articles)}"
        )
        print(f"📰 {title}")
        print(f"🌐 Source: {source}")
        print("========================================")

        # =================================================
        # OPTION A — RSS CONTENT
        # =================================================

        if rss_content and len(rss_content) >= 300:

            print(
                "✅ USING RSS CONTENT"
            )

            print(
                f"📝 RSS content length: "
                f"{len(rss_content)}"
            )

            full_articles.append(
                {
                    "title": title,
                    "url": url,
                    "source": source,
                    "content": rss_content,
                }
            )

            print(
                "✅ ARTICLE ADDED FROM RSS"
            )

            continue

        # =================================================
        # OPTION B — WEBPAGE FALLBACK
        # =================================================

        print(
            "⚠️ RSS content too short."
        )

        print(
            "🌐 Falling back to webpage..."
        )

        webpage_content = scrape_article_content(
            url
        )

        if webpage_content:

            full_articles.append(
                {
                    "title": title,
                    "url": url,
                    "source": source,
                    "content": webpage_content,
                }
            )

            print(
                "✅ ARTICLE ADDED FROM WEBPAGE"
            )

            continue

        # =================================================
        # OPTION C — USE SHORT RSS CONTENT
        # =================================================

        if rss_content:

            print(
                "⚠️ Webpage extraction failed."
            )

            print(
                "✅ Using RSS content as final fallback."
            )

            full_articles.append(
                {
                    "title": title,
                    "url": url,
                    "source": source,
                    "content": rss_content,
                }
            )

            continue

        # =================================================
        # NOTHING AVAILABLE
        # =================================================

        print(
            "❌ Could not obtain usable content."
        )

    # =====================================================
    # FINAL RESULT
    # =====================================================

    print("\n")
    print("========================================")
    print("🎉 SCRAPER FINISHED")
    print("========================================")

    print(
        f"📰 RSS ARTICLES: "
        f"{len(basic_articles)}"
    )

    print(
        f"✅ USABLE ARTICLES: "
        f"{len(full_articles)}"
    )

    if not full_articles:

        print(
            "❌ SCRAPER PRODUCED ZERO USABLE ARTICLES"
        )

    else:

        print(
            "✅ SCRAPER HAS ARTICLES "
            "READY FOR SUMMARIZATION"
        )

    print("========================================")

    return full_articles