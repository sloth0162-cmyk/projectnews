# finance/finance_pipeline.py
from finance.finance_scraper import scrape_news
from services.finance_llm import summarize_finance_article, classify_finance_topic
from services.supabase_client import supabase
from datetime import datetime

def save_finance_article_to_db(title, summary, tag):
    """Insert finance article into separate Supabase table."""
    try:
        supabase.table("finance_articles").insert({
            "title": title,
            "summary": summary,
            "tag": tag,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
    except Exception as e:
        print("⚠️ DB insert error:", e)

def run_finance_pipeline(limit_per_source=3):
    print("🚀 Running finance pipeline…")
    articles = scrape_news(limit_per_source)
    for a in articles:
        summary = summarize_finance_article(a["content"])
        tag = classify_finance_topic(a["content"])
        save_finance_article_to_db(a["title"], summary, tag)
    print("✅ Finance pipeline complete.")

# quick test
if __name__ == "__main__":
    run_finance_pipeline(limit_per_source=1)
