import requests
from bs4 import BeautifulSoup

RSS_FEEDS = [
    {"source": "CNBC Finance", "url": "https://www.cnbc.com/id/10000664/device/rss/rss.html"},
    {"source": "FT Markets", "url": "https://www.ft.com/markets?format=rss"},
    {"source": "Bloomberg", "url": "https://feeds.bloomberg.com/markets/news.rss"},

]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; NewsScraper/1.0)"}

def fetch_all_articles(limit_per_source=3):
    articles = []
    for feed in RSS_FEEDS:
        try:
            response = requests.get(feed["url"], headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item")
        except Exception as e:
            print(f"⚠️ Error fetching {feed['source']}: {e}")
            continue

        for item in items[:limit_per_source]:
            title = item.title.text if item.title else "No title"
            link = item.link.text if item.link else ""
            articles.append({"title": title, "url": link, "source": feed["source"]})
    return articles


def scrape_article_content(url):
    """Scrape main text content."""
    blocked_sites = ["ft.com", "bloomberg.com"]
    if any(site in url for site in blocked_sites):
        return "⚠️ Content may not be publicly accessible."

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "lxml")
        paragraphs = soup.find_all("p")
        content = "\n".join(
            [p.get_text() for p in paragraphs if len(p.get_text().strip()) > 40]
        )
        return content.strip() if content else "⚠️ No readable content found."
    except Exception as e:
        return f"⚠️ Failed to scrape content: {e}"


def scrape_news(limit_per_source=3):
    articles = fetch_all_articles(limit_per_source)
    full_articles = []
    for article in articles:
        content = scrape_article_content(article["url"])
        full_articles.append({**article, "content": content})
    return full_articles


if __name__ == "__main__":
    articles = scrape_news(limit_per_source=2)
    for a in articles:
        print(f"\n=== {a['source']} ===")
        print(f"Title: {a['title']}")
        print(f"URL: {a['url']}")
        print(f"Content: {a['content'][:300]}...\n")
