from supabase import create_client
from config import Config

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_KEY)


def save_summary_to_db(title, summary, image_url):
    data = supabase.table("articles").insert({
        "title": title,
        "summary": summary,
        "image_url": image_url
    }).execute()

    return data