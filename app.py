# app.py
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from agents.scraper_agent import scrape_news
from agents.summarizer_agent import summarize_text
from agents.classifier_agent import classify_article, save_tags_to_article
from services.supabase_client import save_summary_to_db, supabase
from config import Config
from supabase import create_client
from finance.finance_pipeline import run_finance_pipeline
import requests


# -----------------------------
# 🔧 Flask App Setup
# -----------------------------
app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)


# -----------------------------
# 🏠 Home Route
# -----------------------------
@app.route('/')
def home():
    return "🌍 Geo AI Platform Running ✅"


# -----------------------------
# 📰 Dashboard (Main Page)
# -----------------------------
@app.route('/dashboard')
def dashboard_page():
    """Main dashboard displaying summarized geopolitical + finance news"""
    tag = request.args.get("tag")
    search = request.args.get("search", "").strip()

    # Base query
    query = supabase.table("articles").select("*").order("id", desc=True)

    # Tag filter
    if tag and tag.lower() != "all":
        query = query.ilike("tags", f"%{tag}%")

    # Search filter
    if search:
        try:
            query = query.or_(f"title.ilike.%{search}%,summary.ilike.%{search}%")
        except Exception as e:
            print(f"⚠️ Search filter error: {e}")

    # Execute query
    try:
        result = query.execute()
        articles = result.data or []
    except Exception as e:
        print(f"⚠️ Error fetching articles: {e}")
        articles = []

    # Fetch finance preview (for dashboard sidebar/section)
    try:
        finance_result = (
            supabase.table("finance_articles")
            .select("*")
            .order("id", desc=True)
            .limit(6)
            .execute()
        )
        finance_articles = finance_result.data or []
    except Exception as e:
        print(f"⚠️ Error fetching finance_articles: {e}")
        finance_articles = []

    # Add image mapping
    image_map = {
        86: "/static/images/article_86.jpg",
        87: "/static/images/article_87.jpg",
        88: "/static/images/article_88.jpg",
        89: "/static/images/article_89.jpg",
        90: "/static/images/article_90.jpg",
    }
    for a in articles:
        a["image"] = image_map.get(a["id"], "/static/images/default.jpg")

    return render_template(
        "dashboard.html",
        articles=articles,
        finance_articles=finance_articles,
        current_tag=tag or "All",
        search_query=search,
    )


# -----------------------------
# 📄 Additional Pages
# -----------------------------
@app.route("/secondpage")
def second_page():
    tag = request.args.get("tag")
    search = request.args.get("search", "").strip()
     # Tag filter
    if tag and tag.lower() != "all":
        query = query.ilike("tags", f"%{tag}%")

    # Search filter
    if search:
        try:
            query = query.or_(f"title.ilike.%{search}%,summary.ilike.%{search}%")
        except Exception as e:
            print(f"⚠️ Search filter error: {e}")

    # Execute query
    try:
        result = query.execute()
        articles = result.data or []
    except Exception as e:
        print(f"⚠️ Error fetching articles: {e}")
        articles = []
    return render_template("secondpage/secondpage.html",
        articles=articles,
        current_tag=tag or "All",
        search_query=search,)


@app.route("/thirdpage")
def third_page():
    tag = request.args.get("tag")
    search = request.args.get("search", "").strip()
    query = supabase.table("articles").select("*").order("id", desc=True)

    if tag and tag.lower() != "all":
        query = query.ilike("tags", f"%{tag}%")

    result = query.execute()
    articles = result.data or []
     # Search filter
    if search:
        try:
            query = query.or_(f"title.ilike.%{search}%,summary.ilike.%{search}%")
        except Exception as e:
            print(f"⚠️ Search filter error: {e}")

    # Execute query
    try:
        result = query.execute()
        articles = result.data or []
    except Exception as e:
        print(f"⚠️ Error fetching articles: {e}")
        articles = []


    return render_template(
        "thirdpage.html",
        articles=articles,
        search_query=search,
        current_tag=tag or "All"
    )


# -----------------------------
# 🔐 Google Auth (via Supabase)
# -----------------------------
@app.route("/auth/login")
def login_google():
    """Redirect user to Supabase Google OAuth."""
    redirect_url = f"{Config.SUPABASE_URL}/auth/v1/authorize?provider=google&redirect_to=http://127.0.0.1:5000/auth/callback"
    return redirect(redirect_url)


@app.route("/auth/callback")
def auth_callback():
    """Handle redirect from Supabase Google login."""
    access_token = request.args.get("access_token")

    if not access_token:
        # Simulate login (for now)
        session["logged_in"] = True
        return redirect(url_for("dashboard_page"))

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{Config.SUPABASE_URL}/auth/v1/user", headers=headers)

    if response.status_code == 200:
        user = response.json()
        session["user"] = user
        print("✅ Logged in user:", user.get("email"))
    else:
        print("❌ Failed to verify user token:", response.text)

    return redirect(url_for("dashboard_page"))


# -----------------------------
# ⚙️ Run News Pipeline (General)
# -----------------------------
@app.route('/run_pipeline', methods=['POST', 'GET'])
def run_pipeline():
    """Scrapes general news → summarizes → saves to Supabase."""
    articles = scrape_news(limit_per_source=2)

    for article in articles:
        title = article['title']
        content = article['content']

        # Skip if article already exists
        exists = supabase.table('articles').select('id').eq('title', title).execute()
        if exists.data:
            print(f"⏭️ Skipping existing article: {title}")
            continue

        print(f"🧠 Summarizing: {title}")
        summary = summarize_text(content)
        save_summary_to_db(title, summary)

    return {"status": "success", "articles_processed": len(articles)}


# -----------------------------
# 🧠 Editorial (Manual Posts)
# -----------------------------
@app.route('/editorial')
def editorial_page():
    return render_template('editorial.html')


# -----------------------------
# 💰 Finance Section
# -----------------------------
@app.route("/finance")
def finance_page():
    """Finance dashboard route."""
    try:
        result = (
            supabase.table("finance_articles")
            .select("*")
            .order("id", desc=True)
            .execute()
        )
        articles = result.data or []
    except Exception as e:
        print("⚠️ Error fetching finance articles:", e)
        articles = []

    return render_template("finance/index.html", articles=articles)


@app.route("/run_finance_pipeline")
def run_finance_route():
    """Run finance-specific scraping + summarization pipeline."""
    run_finance_pipeline(limit_per_source=2)
    return "✅ Finance pipeline executed successfully!"


# -----------------------------
# 🚀 App Launcher
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
