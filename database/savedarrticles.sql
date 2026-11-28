from flask import Blueprint, render_template
from services.supabase_client import supabase

article_bp = Blueprint("article", __name__)


@article_bp.route("/article/<int:article_id>")
def article(article_id):
    try:
        result = (
            supabase
            .table("articles")
            .select("*")
            .eq("id", article_id)
            .execute()
        )
        articles_data = result.data or []
    except Exception as e:
        print(f"⚠️ Error fetching article #{article_id}: {e}")
        articles_data = []

    if not articles_data:
        return render_template("article.html", article=None, related_articles=[]), 404

    target_article = articles_data[0]

    # Fetch recent related stories
    related_articles = []
    try:
        related_result = (
            supabase
            .table("articles")
            .select("*")
            .neq("id", article_id)
            .order("id", desc=True)
            .limit(4)
            .execute()
        )
        related_articles = related_result.data or []
    except Exception as e:
        print(f"⚠️ Error fetching related articles: {e}")

    return render_template(
        "article.html",
        article=target_article,
        related_articles=related_articles
    )
