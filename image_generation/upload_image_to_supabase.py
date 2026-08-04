import mimetypes
from pathlib import Path
import uuid

from services.supabase_client import supabase

BUCKET_NAME = "article-images"

storage = supabase.storage.from_(BUCKET_NAME)


def upload_image(image_path):
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    filename = f"{uuid.uuid4()}{image_path.suffix}"

    content_type, _ = mimetypes.guess_type(str(image_path))
    content_type = content_type or "application/octet-stream"

    with open(image_path, "rb") as image:
        storage.upload(
            path=filename,
            file=image,
            file_options={
                "content-type": content_type,
            },
        )

    public_url = storage.get_public_url(filename)
    print(public_url)

    return public_url