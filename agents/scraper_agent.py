"""
News scraper rewritten for Vercel Hobby (10s function timeout, read-only FS
except /tmp, no guarantee lxml is present).

KEY FIXES vs the old version:
1. Root cause of "works locally, fails on Vercel": BeautifulSoup(content, "xml")
   silently depends on `lxml` being installed. If it's missing from
   requirements.txt, this either throws bs4.FeatureNotFound or just returns
   zero <item> tags -> logged as "RSS returned no items" and swallowed.
   Fix: use `feedparser`, a pure-Python RSS/Atom parser with no lxml
   dependency and much better tolerance of malformed/varied feed formats.
2. Old timeouts (10s connect, 15s read) PER REQUEST are incompatible with a
   10s total function budget. Fixed with short per-request timeouts and a
   hard overall deadline enforced with a wall-clock check, not just
   per-request timeouts.
3. Feeds are fetched concurrently (ThreadPoolExecutor) instead of serially,
   since serial fetching of 4 feeds can alone exceed 10s if any one feed is
   slow.
4. Full-article-page scraping (scrape_article_content) is OFF by default on
   serverless, because a single slow site can eat the whole time budget.
   It's controlled by ALLOW_ARTICLE_SCRAPE / remaining time budget.
5. All diagnostics are returned as structured data (not just printed), so
   the caller (pipeline route) can surface real failure reasons to you
   instead of them vanishing into Vercel's function logs.

Add to requirements.txt:
    feedparser
    requests
    beautifulsoup4
(lxml is no longer required for feed parsing; keep it only if you still want
 scrape_article_content's HTML parsing to use a faster parser — html.parser
 is stdlib and works fine without it.)
"""

import time
import feedparser
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed


RSS_FEEDS = [
    {"source": "BBC", "url": "https://feeds.bbci.co.uk/news/world/rss.xml"},
    {"source": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml"},
    {"source": "FT", "url": "https://www.ft.com/?format=rss"},
    {"source": "CNBC", "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html"},
]

MAX_ARTICLES = 4

# --- Serverless time budget (Hobby plan = 10s hard limit) -------------------
# Leave headroom for whatever the caller (pipeline route) does after this
# returns. Scraping alone should not eat the whole budget.
SCRAPE_TIME_BUDGET_SECONDS = 6.0

# Per-request timeouts must be short since we have ~6s total, not per-call.
FEED_TIMEOUT = (3, 4)      # (connect, read)
ARTICLE_TIMEOUT = (3, 3)   # (connect, read)

# Full article-page scraping is expensive and unreliable under a tight
# budget. Only attempt it if there's meaningfully more than a couple of
# seconds of budget left, and never as a blocking requirement.
ALLOW_ARTICLE_SCRAPE = False
MIN_CONTENT_LENGTH = 300

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
}


def create_session():
    session = requests.Session()

    retry = Retry(
        total=1,               # serverless: fail fast, don't burn the budget retrying
        connect=1,
        read=1,
        status=1,
        backoff_factor=0.2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
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
    return " ".join(soup.get_text(" ", strip=True).split())


def extract_rss_content(entry):
    """feedparser normalizes description/summary/content across RSS+Atom
    into predictable attributes, so this is much simpler and more robust
    than manually walking XML tags."""

    # feedparser puts the richest version in `.content` (Atom-style) when present
    if getattr(entry, "content", None):
        for block in entry.content:
            text = clean_text(block.get("value", ""))
            if text:
                return text

    if getattr(entry, "summary", None):
        text = clean_text(entry.summary)
        if text:
            return text

    if getattr(entry, "description", None):
        text = clean_text(entry.description)
        if text:
            return text

    return ""


def scrape_article_content(url, deadline):
    """Best-effort full-article fetch. Returns "" on any failure or if we're
    out of time budget — this must never be what makes the pipeline fail."""

    if time.monotonic() >= deadline:
        return ""

    try:
        response = session.get(
            url, timeout=ARTICLE_TIMEOUT, allow_redirects=True
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for selector in [
            "article",
            "[class*='article-body']",
            "[class*='article-content']",
            "[class*='story-body']",
            "[class*='story-content']",
            "main",
        ]:
            for element in soup.select(selector):
                text = " ".join(element.get_text(" ", strip=True).split())
                if len(text) >= MIN_CONTENT_LENGTH:
                    return text

        paragraphs = [
            " ".join(p.get_text(" ", strip=True).split())
            for p in soup.find_all("p")
        ]
        paragraphs = [p for p in paragraphs if len(p) >= 30]
        content = " ".join(paragraphs)

        return content if len(content) >= MIN_CONTENT_LENGTH else ""

    except Exception as e:
        print(f"⚠️ Article scrape failed for {url}: {type(e).__name__}: {e}")
        return ""


def _fetch_one_feed(feed):
    """Runs in a worker thread. Returns (source, entries, error_or_None)."""
    source = feed["source"]
    url = feed["url"]

    try:
        response = session.get(url, timeout=FEED_TIMEOUT, allow_redirects=True)
        response.raise_for_status()

        parsed = feedparser.parse(response.content)

        if parsed.bozo and not parsed.entries:
            # bozo=True means feedparser hit a parse issue. If it still
            # extracted entries, we proceed anyway (feedparser is lenient
            # on purpose). Only treat it as fatal if there's nothing usable.
            reason = getattr(parsed, "bozo_exception", "unknown parse error")
            return source, [], f"{source}: feed parse error: {reason}"

        if not parsed.entries:
            return source, [], f"{source}: RSS returned no items"

        return source, parsed.entries, None

    except requests.exceptions.Timeout:
        return source, [], f"{source}: request timed out"
    except Exception as e:
        return source, [], f"{source}: {type(e).__name__}: {e}"


def fetch_all_articles(errors):
    articles = []
    deadline = time.monotonic() + SCRAPE_TIME_BUDGET_SECONDS

    # Fetch all feeds concurrently instead of serially so one slow feed
    # doesn't consume the whole time budget by itself.
    with ThreadPoolExecutor(max_workers=len(RSS_FEEDS)) as pool:
        futures = {pool.submit(_fetch_one_feed, feed): feed for feed in RSS_FEEDS}

        for future in as_completed(futures, timeout=SCRAPE_TIME_BUDGET_SECONDS + 1):
            if len(articles) >= MAX_ARTICLES:
                break

            try:
                source, entries, error = future.result()
            except Exception as e:
                feed = futures[future]
                errors.append(f"{feed['source']}: {type(e).__name__}: {e}")
                continue

            if error:
                errors.append(error)
                continue

            # Take the first usable entry from this feed.
            for entry in entries:
                if len(articles) >= MAX_ARTICLES:
                    break

                title = clean_text(getattr(entry, "title", ""))
                link = getattr(entry, "link", "").strip()

                if not title or not link:
                    continue

                content = extract_rss_content(entry)

                if len(content) < MIN_CONTENT_LENGTH and ALLOW_ARTICLE_SCRAPE:
                    content = scrape_article_content(link, deadline)

                if not content:
                    print(f"⚠️ No usable content: {title}")
                    continue

                articles.append(
                    {"title": title, "url": link, "source": source, "content": content}
                )
                print(f"✅ Added: {source} - {title}")
                break  # one article per feed

    return articles


def scrape_news():
    print("\n🚀 NEWS SCRAPER STARTED")

    errors = []
    start = time.monotonic()

    articles = fetch_all_articles(errors)

    elapsed = time.monotonic() - start
    scrape_news.last_errors = errors
    scrape_news.last_elapsed_seconds = round(elapsed, 2)

    print(f"📊 Scraper finished in {elapsed:.2f}s — {len(articles)} articles, {len(errors)} errors")
    for error in errors:
        print(f"   - {error}")

    if not articles:
        message = (
            "Scraper failed: no usable articles from any feed. "
            f"Errors: {errors if errors else 'none captured'}"
        )
        print(f"❌ {message}")
        raise RuntimeError(message)

    return articles[:MAX_ARTICLES]


scrape_news.last_errors = []
scrape_news.last_elapsed_seconds = 0.0