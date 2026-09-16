# agents/classifier_agent.py

from services.llm_utils import generate_summary
from services.supabase_client import supabase


ALLOWED_TAGS = {
    "India",
    "Finance",
    "Economy",
    "Geopolitics",
    "Technology",
    "Energy",
    "Global",
    "Conflict",
    "Market",
    "Policy",
}


def classify_article(title, summary):
    """
    Use AI to classify an article into 2-3 allowed tags.
    Returns a list of valid tags.
    """

    prompt = f"""
Analyze this news article and choose 2-3 tags that best describe its main topic.

You may ONLY use these tags:
India, Finance, Economy, Geopolitics, Technology,
Energy, Global, Conflict, Market, Policy

Return ONLY the tag names separated by commas.
Do NOT write explanations.
Do NOT write a sentence.
Do NOT add any other words.

Title: {title}
Summary: {summary}
"""

    response = generate_summary(prompt)

    if not response:
        return []

    raw_tags = response.split(",")

    tags = []

    for raw_tag in raw_tags:
        tag = raw_tag.strip()

        for allowed_tag in ALLOWED_TAGS:
            if tag.lower() == allowed_tag.lower():
                if allowed_tag not in tags:
                    tags.append(allowed_tag)
                break

    return tags[:3]


def save_tags_to_article(title, tags):
    """
    Update the article's tags in Supabase.
    """

    data = (
        supabase
        .table("articles")
        .update({
            "tags": tags
        })
        .eq("title", title)
        .execute()
    )

    return data


def classify_and_update_articles():
    """
    Fetch articles without tags, classify them,
    and update their tags in Supabase.
    """

    result = (
        supabase
        .table("articles")
        .select("*")
        .execute()
    )

    articles = result.data or []

    for article in articles:
        if article.get("tags"):
            continue

        title = article.get("title", "")
        summary = article.get("summary", "")

        if not title or not summary:
            continue

        tags = classify_article(title, summary)

        if not tags:
            print(f"[!] No valid tags generated for '{title}'")
            continue

        save_tags_to_article(title, tags)

        print(f"[+] Classified '{title}' → Tags: {tags}")


# For testing
if __name__ == "__main__":
    classify_and_update_articles()