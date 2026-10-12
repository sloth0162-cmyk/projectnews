from flask import Blueprint, render_template
from services.supabase_client import supabase

second = Blueprint("second", __name__)


def get_articles_by_tag(tag, limit=12):
    try:
        result = (
            supabase.table("articles")
            .select("*")
            .contains("tags", [tag])
            .order("id", desc=True)
            .limit(limit)
            .execute()
        )

        articles = result.data or []

        print(
            f"[secondpage] Tag: {tag!r} | "
            f"Articles found: {len(articles)}"
        )

        return articles

    except Exception as e:
        print(f"[secondpage] ERROR for tag {tag!r}: {e}")
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
