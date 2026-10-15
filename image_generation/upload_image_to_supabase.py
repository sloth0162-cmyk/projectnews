import uuid

from services.supabase_client import supabase

BUCKET_NAME = "article-images"

storage = supabase.storage.from_(BUCKET_NAME)


def upload_image(image_bytes):
    if not image_bytes:
        raise ValueError("No image data to upload")

    # Same naming scheme as before: random UUID + .png
    # (the old suffix came from "generated_images/test.png")
    filename = f"{uuid.uuid4()}.png"

    storage.upload(
        path=filename,
        file=image_bytes,
        file_options={
            "content-type": "image/png",
        },
    )

    public_url = storage.get_public_url(filename)
    print(public_url)

    return public_url