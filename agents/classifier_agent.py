# agents/classifier_agent.py

from services.llm_utils import generate_summary
from services.supabase_client import supabase

def classify_article(title, summary):
    """
    Use AI to classify article into tags (Finance, Geopolitics, etc.)
    Returns a list of tags.
    """
    prompt = f"""
    Analyze this news and return 2-3 short tags related to its main topic.
    Only choose from: India, Finance, Economy, Geopolitics, Technology, Energy, Global, Conflict, Market, Policy.
    Title: {title}
    Summary: {summary}
    Return tags as a comma-separated list.
    """

    response = generate_summary(prompt)  # Using your existing LLM helper
    # Example output: "Finance, Market, India"
    tags = [tag.strip() for tag in response.split(",") if tag.strip()]
    return tags

def save_tags_to_article(title, tags):
    """
    Updates the article in Supabase with generated tags.
    """
    data = supabase.table("articles").update({
        "tags": tags
    }).eq("title", title).execute()
    return data

def classify_and_update_articles():
    """
    Fetch recent articles without tags and classify them.
    """
    result = supabase.table("articles").select("*").execute()
    articles = result.data

    for article in articles:
        if not article.get("tags"):
            title = article["title"]
            summary = article["summary"]
            tags = classify_article(title, summary)
            save_tags_to_article(title, tags)
            print(f"[+] Classified '{title}' → Tags: {tags}")

# For testing:
if __name__ == "__main__":
    classify_and_update_articles()
