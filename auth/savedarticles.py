from flask import Blueprint, jsonify, session, request
from services.supabase_client import supabase

saved_articles_bp = Blueprint("saved_articles", __name__)


def get_saved_articles(user_id):
    try:
        result = (
            supabase.table("saved_articles")
            .select("created_at, articles(*)")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

        return [
            row["articles"]
            for row in (result.data or [])
            if row.get("articles")
        ]

    except Exception as error:
        print("Error fetching saved articles:", error)
        return []


@saved_articles_bp.route(
    "/saved-articles/<int:article_id>",
    methods=["POST", "DELETE"]
)
def manage_saved_article(article_id):
    user = session.get("user")

    if not user:
        return jsonify({
            "success": False,
            "message": "Please sign in first."
        }), 401

    try:
        if request.method == "POST":
            (
                supabase.table("saved_articles")
                .upsert(
                    {
                        "user_id": user["id"],
                        "article_id": article_id
                    },
                    on_conflict="user_id,article_id",
                    ignore_duplicates=True
                )
                .execute()
            )

            return jsonify({
                "success": True,
                "saved": True
            })

        (
            supabase.table("saved_articles")
            .delete()
            .eq("user_id", user["id"])
            .eq("article_id", article_id)
            .execute()
        )

        return jsonify({
            "success": True,
            "saved": False
        })

    except Exception as error:
        print("Saved article error:", error)

        return jsonify({
            "success": False,
            "message": "Unable to update saved articles."
        }), 500