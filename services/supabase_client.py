from supabase import create_client
from config import Config
import os
# Create Supabase client using environment variables
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)



def save_summary_to_db(title, summary):
    data = supabase.table("articles").insert({
        "title": title,
        "summary": summary
    }).execute()
    return data

