from flask import Blueprint, render_template
from services.supabase_client import supabase

article_bp = Blueprint("article", __name__)


@article_bp.route("/article/<int:article_id>")
def article(article_id):

    result = (
        supabase
        .table("articles")
        .select("*")
        .eq("id", article_id)
        .execute()
    )

    article = result.data

    if not article:
        return "Article not found", 404

    return render_template(
        "article.html",
        article=article[0]
    )