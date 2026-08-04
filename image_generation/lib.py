import os
from pathlib import Path

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
    output_file="generated_images/test.png",
):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

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

    with open(output_path, "wb") as image:
        image.write(response.content)

    print(f"✅ Image generated successfully!")
    print(f"📁 Saved as: {output_path}")

    return str(output_path)