from image_generation.lib import generate_image

def build_prompt(title, summary):
    return (
        "Create a realistic news illustration based on the following article.\n\n"
        f"Title: {title}\n"
        f"Summary: {summary}\n\n"
        "Requirements:\n"
        "- No text or captions in the image.\n"
        "- No logos or watermarks.\n"
        "- Realistic, high quality.\n"
        "- Focus on the main event described."
    )

def create_news_image(title, summary):
    prompt = build_prompt(title, summary)
    return generate_image(prompt)