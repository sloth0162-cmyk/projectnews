# services/llm_utils.py

import os
import requests


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL = "meta-llama/llama-3.1-8b-instruct"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def generate_summary(text: str):

    print("\n========================================")
    print("🧠 OPENROUTER SUMMARY START")
    print("========================================")

    # -----------------------------------------
    # Check API key
    # -----------------------------------------

    if not OPENROUTER_API_KEY:

        print("❌ OPENROUTER_API_KEY IS MISSING")
        print("❌ Check Vercel Environment Variables")

        return ""

    print("✅ OPENROUTER_API_KEY FOUND")
    print(f"🤖 Model: {MODEL}")

    # -----------------------------------------
    # Validate input
    # -----------------------------------------

    if not text:

        print("❌ Empty article text")
        return ""

    print(
        f"📝 Original text length: "
        f"{len(text)} characters"
    )

    short_text = text[:3000]

    print(
        f"📝 Sending: "
        f"{len(short_text)} characters"
    )

    # -----------------------------------------
    # Headers
    # -----------------------------------------

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://projectnews-mocha.vercel.app",
        "X-Title": "Sloth Newz"
    }

    # -----------------------------------------
    # Payload
    # -----------------------------------------

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional news editor. "
                    "Read the provided article carefully and write "
                    "a concise, engaging paragraph summarizing the "
                    "key events and context. "
                    "Use natural, human language like a journalist "
                    "writing a short news brief. "
                    "Avoid lists, bullet points, or phrases like "
                    "'the article discusses' or 'in summary'. "
                    "Keep the tone factual, neutral, and easy to "
                    "read for a general audience."
                )
            },
            {
                "role": "user",
                "content": short_text
            }
        ]
    }

    # -----------------------------------------
    # API request
    # -----------------------------------------

    try:

        print("📡 Sending request to OpenRouter...")

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        print("✅ OpenRouter responded")
        print(
            f"📡 Status Code: "
            f"{response.status_code}"
        )

        print(
            f"📦 Response Size: "
            f"{len(response.content)} bytes"
        )

    except requests.exceptions.Timeout:

        print("⏰ OPENROUTER TIMEOUT")
        return ""

    except requests.exceptions.RequestException as e:

        print("❌ OPENROUTER NETWORK ERROR")
        print(f"❌ Error type: {type(e).__name__}")
        print(f"❌ Error: {e}")

        return ""

    # -----------------------------------------
    # Handle API errors
    # -----------------------------------------

    if response.status_code != 200:

        print("\n========================================")
        print("❌ OPENROUTER API ERROR")
        print("========================================")

        print(
            f"📡 Status: "
            f"{response.status_code}"
        )

        print(
            f"📄 Response:"
            f"\n{response.text[:1000]}"
        )

        return ""

    # -----------------------------------------
    # Parse response
    # -----------------------------------------

    try:

        data = response.json()

        print("✅ JSON parsed successfully")

        summary = (
            data["choices"][0]["message"]["content"]
            .strip()
        )

        if not summary:

            print("❌ OpenRouter returned empty summary")
            return ""

        print("✅ SUMMARY GENERATED")
        print(
            f"📝 Summary length: "
            f"{len(summary)} characters"
        )

        print("========================================")

        return summary

    except (KeyError, IndexError, ValueError) as e:

        print("❌ INVALID OPENROUTER RESPONSE")

        print(
            f"❌ Error type: "
            f"{type(e).__name__}"
        )

        print(
            f"❌ Error: {e}"
        )

        print(
            f"📄 Raw response:"
            f"\n{response.text[:1000]}"
        )

        return ""

    except Exception as e:

        print("❌ UNEXPECTED OPENROUTER ERROR")
        print(
            f"❌ Error type: "
            f"{type(e).__name__}"
        )
        print(f"❌ Error: {e}")

        return ""