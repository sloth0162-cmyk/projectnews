# services/llm_utils.py

import requests
import json

# ⚠️ Replace this with your actual key (no leading space)
OPENROUTER_API_KEY = "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"
MODEL = "meta-llama/llama-3-8b-instruct"


def generate_summary(text: str):
    """Generate a short, engaging paragraph-style summary of a news article using OpenRouter."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    short_text = text[:3000]  # Safety limit

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000/",
        "X-Title": "Geo AI Platform"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional news editor. "
                    "Read the provided article carefully and write a concise, engaging paragraph summarizing the key events and context. "
                    "Use natural, human language like a journalist writing a short news brief. "
                    "Avoid lists, bullet points, or phrases like 'the article discusses' or 'in summary'. "
                    "Keep the tone factual, neutral, and easy to read for a general audience."
                ),
            },
            {
                "role": "user",
                "content": f"{short_text}"
            }
        ],
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
    except requests.exceptions.RequestException as e:
        print(f"\n--- NETWORK ERROR ---\n{e}\n---------------------\n")
        return "Error: Network issue while connecting to OpenRouter"

    if response.status_code == 200:
        try:
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, ValueError):
            return "Error: Unexpected response format from OpenRouter"
    else:
        print("\n--- OPENROUTER API ERROR ---")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text[:500])
        print("-----------------------------\n")
        return f"Error generating summary ({response.status_code})"
