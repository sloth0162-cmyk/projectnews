import os

import requests
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

API_BASE_URL = (
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/"
)

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}


def generate_image(
    prompt,
    model="@cf/lykon/dreamshaper-8-lcm",
):
    payload = {
        "prompt": prompt
    }

    response = requests.post(
        f"{API_BASE_URL}{model}",
        headers=HEADERS,
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    print("✅ Image generated successfully!")

    return response.content  # image bytes, nothing written to disk