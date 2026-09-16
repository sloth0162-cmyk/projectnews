# services/finance_llm.py

from services.llm_utils import generate_summary


def summarize_finance_article(text: str):
    """
    Generate a short summary for a finance article
    using the shared OpenRouter configuration.
    """

    if not text:
        return ""

    prompt = f"""
You are a senior financial journalist.

Read the following finance article and write a concise,
human-readable summary.

Focus on:
- what happened
- why it matters
- the financial, market, or economic impact

Write one natural paragraph.
Do not use bullet points.
Do not mention that you are summarizing an article.
Keep it under 100 words.

Article:
{text[:3500]}
"""

    return generate_summary(prompt)


def classify_finance_topic(text: str):
    """
    Classify a finance article into exactly one category.
    """

    if not text:
        return "Uncategorized"

    prompt = f"""
Classify this finance article into exactly ONE category.

Allowed categories:
Stock
Crypto
Business
Economy
Policy

Return ONLY one category word.
Do not add an explanation.

Article:
{text[:1200]}
"""

    response = generate_summary(prompt)

    if not response:
        return "Uncategorized"

    response = response.strip()

    allowed_categories = {
        "Stock",
        "Crypto",
        "Business",
        "Economy",
        "Policy",
    }

    for category in allowed_categories:
        if response.lower() == category.lower():
            return category

    return "Uncategorized"