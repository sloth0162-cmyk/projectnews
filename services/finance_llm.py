# services/finance_llm.py
import requests
import json

OPENROUTER_API_KEY = "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"  # 🔑 replace
MODEL = "meta-llama/llama-3-8b-instruct"  # bad finance reasoning model
BASE_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:5000/",
    "X-Title": "FinanceAI Platform"
}


def summarize_finance_article(text: str):
    """Generate a short, human-like paragraph summarizing a finance article."""
    short_text = text[:3500]

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a senior financial journalist writing for Bloomberg or Reuters. "
                    "Read the article and craft a single, concise paragraph summarizing the key financial developments. "
                    "Focus on what happened, why it matters, and the market or economic impact — "
                    "but write it in a natural, human tone that sounds like professional news copy. "
                    "Avoid bullet points, lists, and meta instructions. "
                    "Keep it under 100 words, clear, factual, and fluid."
                ),
            },
            {"role": "user", "content": short_text},
        ],
    }

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=BASE_HEADERS,
            data=json.dumps(payload),
            timeout=25
        )
        if r.status_code == 200:
            data = r.json()
            return data["choices"][0]["message"]["content"].strip()
        else:
            print("\n--- OPENROUTER FINANCE API ERROR ---")
            print("Status Code:", r.status_code)
            print("Response Text:", r.text[:300])
            print("------------------------------------\n")
            return f"Error generating finance summary ({r.status_code})"
    except Exception as e:
        print("⚠️ Finance summarization error:", e)
        return "Error generating summary."


def classify_finance_topic(text: str):
    """Return one category: Stock, Crypto, Business, Economy, Policy."""
    short_text = text[:1200]

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Classify this financial article into exactly ONE category word from: "
                    "[Stock, Crypto, Business, Economy, Policy]. "
                    "Return only the single word, no explanation."
                ),
            },
            {"role": "user", "content": short_text},
        ],
    }

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=BASE_HEADERS,
            data=json.dumps(payload),
            timeout=20
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("⚠️ Finance tag error:", e)
        return "Uncategorized"