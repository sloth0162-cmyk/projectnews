from flask import Blueprint, render_template
from supabase import create_client
from config import Config
second = Blueprint("second", __name__)

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
def get_articles_by_tag(tag, limit=12):
    """Fetch articles matching a specific tag."""
    try:
        result = (
            supabase.table("articles")
            .select("*")
            .contains("tags", [tag])
            .order("id", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data or []

    except Exception as e:
        print(f"Error fetching articles for tag '{tag}': {e}")
        return []


@second.route("/")
def secondpage():
    return render_template(
        "secondpage/secondpage.html",
        crypto_articles=get_articles_by_tag("Crypto"),
        business_articles=get_articles_by_tag("Finance"),
        indianmarket_articles=get_articles_by_tag("India"),
        realestate_articles=get_articles_by_tag("Real Estate"),
        commodities_articles=get_articles_by_tag("Energy"),
        tech_articles=get_articles_by_tag("Technology"),
        stockmarket_articles=get_articles_by_tag("Market"),
    )