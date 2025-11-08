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
        response = requests.get(feed["url"])
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all('item')
        
        for item in items[:limit_per_source]:
            title = item.title.text
            link = item.link.text
            articles.append({
                "title": title,
                "url": link,
                "source": feed["source"]
            })
    return articles

def scrape_article_content(url):
    """Scrape article content from URL (generic, works for most sites)."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all('p')
    content = "\n".join([p.get_text() for p in paragraphs])
    return content.strip()

def scrape_news(limit_per_source=3):
    """Return list of full article data."""
    basic_articles = fetch_all_articles(limit_per_source)
    full_articles = []
    
    for article in basic_articles:
        content = scrape_article_content(article["url"])
        full_articles.append({
            "title": article["title"],
            "url": article["url"],
            "source": article["source"],
            "content": content
        })
    return full_articles

# Test
if __name__ == "__main__":
    articles = scrape_news(limit_per_source=2)
    for article in articles:
        print("\n=== Article ===")
        print("Source:", article["source"])
        print("Title:", article["title"])
        print("URL:", article["url"])
        print("Content:", article["content"][:300], "...")
