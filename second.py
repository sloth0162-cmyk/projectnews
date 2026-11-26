
from flask import Blueprint, render_template, request, jsonify
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


# ---------------------------------
# NEWSLETTER SUBSCRIPTION
# ---------------------------------

@second.route("/subscribe", methods=["POST"])
def subscribe_newsletter():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()

    if not email or "@" not in email:
        return jsonify({
            "success": False,
            "message": "Please enter a valid email address."
        }), 400

    try:
        existing = (
            supabase.table("newsletter_subscribers")
            .select("id, is_active")
            .eq("email", email)
            .execute()
        )

        if existing.data:
            subscriber = existing.data[0]

            if subscriber["is_active"]:
                return jsonify({
                    "success": False,
                    "message": "You're already subscribed!"
                }), 409

            supabase.table("newsletter_subscribers").update({
                "is_active": True
            }).eq("email", email).execute()

        else:
            supabase.table("newsletter_subscribers").insert({
                "email": email
            }).execute()

        return jsonify({
            "success": True,
            "message": "Welcome to Sloth News Intelligence Briefing!"
        })

    except Exception as e:
        print(f"[newsletter] ERROR: {e}")

        return jsonify({
            "success": False,
            "message": "Subscription failed. Please try again later."
        }), 500
