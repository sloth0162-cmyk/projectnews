import os
import base64
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
    model="@cf/black-forest-labs/flux-1-schnell",
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

    if not response.ok:
        print(f"Cloudflare status: {response.status_code}")
        print(f"Cloudflare response: {response.text[:1500]}")

    response.raise_for_status()

    data = response.json()

    if not data.get("success"):
        raise RuntimeError(
            f"Cloudflare AI error: {data.get('errors')}"
        )

    image_base64 = data["result"]["image"]

    print("✅ Image generated successfully!")

    return base64.b64decode(image_base64)