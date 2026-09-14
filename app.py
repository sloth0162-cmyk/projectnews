# app.py
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for, session
from agents.scraper_agent import scrape_news
from agents.summarizer_agent import summarize_text
from agents.classifier_agent import classify_article, save_tags_to_article
from services.supabase_client import save_summary_to_db, supabase
from config import Config
from supabase import create_client
from finance.finance_pipeline import run_finance_pipeline
import requests
from image_generation.image_generate import create_news_image
from image_generation.upload_image_to_supabase import upload_image
from routes.route import article_bp
from second import second

# -----------------------------
# 🔧 Flask App Setup
# -----------------------------
app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

PIPELINE_PASSWORD = Config.PIPELINE_PASSWORD
app.register_blueprint(article_bp)
app.register_blueprint(second)

# -----------------------------
# 📰 Dashboard (Main Page)
# -----------------------------
@app.route('/')
def dashboard_page():
    """Main dashboard displaying summarized news"""
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
   #test below
    for a in articles[:3]:
        print(a)
    print(articles[0])

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
@app.route('/run_pipeline', methods=['GET', 'POST'])
def run_pipeline():

    # -----------------------------
    # GET → Show pipeline page
    # -----------------------------
    if request.method == 'GET':
        return render_template('pipeline/run_pipeline.html')

    # -----------------------------
    # Check password
    # -----------------------------
    password = request.form.get('password')

    if password != PIPELINE_PASSWORD:
        print("❌ Pipeline rejected: Incorrect password")

        return render_template(
            'pipeline/run_pipeline.html',
            error="Incorrect password"
        )

    print("\n========================================")
    print("🚀 PIPELINE STARTED")
    print("========================================")

    # -----------------------------
    # 1. SCRAPE NEWS
    # -----------------------------
    print("\n🔎 STEP 1: Starting news scraper...")

    try:
        articles = scrape_news(limit_per_source=1)

        print("✅ scrape_news() returned successfully")
        print(f"📰 Articles returned: {len(articles)}")

    except Exception as e:
        print("❌ SCRAPER FAILED")
        print(f"❌ Error type: {type(e).__name__}")
        print(f"❌ Error: {e}")

        return render_template(
            'pipeline/run_pipeline.html',
            error=f"Scraper failed: {e}"
        )

    # Nothing returned
    if not articles:
        print("⚠️ SCRAPER RETURNED ZERO ARTICLES")
        print("🏁 Pipeline stopped because there is nothing to process.")

        return render_template(
            'pipeline/run_pipeline.html',
            error="No new articles were returned by the scraper."
        )

    # -----------------------------
    # 2. PROCESS ARTICLES
    # -----------------------------
    print(f"\n📦 STEP 2: Processing {len(articles)} articles...")

    for index, article in enumerate(articles, start=1):

        print("\n========================================")
        print(f"📄 ARTICLE {index}/{len(articles)}")
        print("========================================")

        title = article.get('title', '')
        content = article.get('content', '')

        print(f"📰 Title: {title}")
        print(f"🌐 Source: {article.get('source', 'Unknown')}")
        print(f"🔗 URL: {article.get('url', 'Unknown')}")
        print(f"📝 Content length: {len(content)} characters")

        if not title:
            print("⚠️ Article has no title. Skipping.")
            continue

        if not content:
            print("⚠️ Article has no content. Skipping.")
            continue

        # -----------------------------
        # 3. CHECK SUPABASE
        # -----------------------------
        print("\n🔎 STEP 3: Checking Supabase for duplicate...")

        try:

            exists = supabase.table('articles') \
                .select('id') \
                .eq('title', title) \
                .execute()

            print("✅ Supabase duplicate check completed")
            print(f"🔎 Matching articles: {len(exists.data)}")

        except Exception as e:

            print("❌ SUPABASE DUPLICATE CHECK FAILED")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Error: {e}")

            continue

        if exists.data:
            print(f"⏭️ Article already exists. Skipping:")
            print(f"   {title}")
            continue

        print("🆕 Article is NEW")


        # -----------------------------
        # 4. SUMMARIZE
        # -----------------------------
        print("\n🧠 STEP 4: Starting summarizer...")

        try:

            summary = summarize_text(content)

            if not summary:
                print("❌ SUMMARIZER RETURNED EMPTY RESULT")
                print(f"❌ Article skipped: {title}")
                continue

            print("✅ SUMMARIZER SUCCESS")
            print(f"📝 Summary length: {len(summary)} characters")

        except Exception as e:

            print("❌ SUMMARIZER FAILED")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Error: {e}")

            continue


        # -----------------------------
        # 5. GENERATE IMAGE
        # -----------------------------
        print("\n🎨 STEP 5: Starting image generation...")

        try:

            image_path = create_news_image(
                title,
                summary
            )

            if not image_path:
                print("❌ IMAGE GENERATION RETURNED EMPTY RESULT")
                continue

            print("✅ IMAGE GENERATION SUCCESS")
            print(f"🖼️ Image path: {image_path}")

        except Exception as e:

            print("❌ IMAGE GENERATION FAILED")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Error: {e}")

            continue


        # -----------------------------
        # 6. UPLOAD IMAGE
        # -----------------------------
        print("\n☁️ STEP 6: Uploading image...")

        try:

            image_url = upload_image(image_path)

            if not image_url:
                print("❌ IMAGE UPLOAD RETURNED EMPTY RESULT")
                continue

            print("✅ IMAGE UPLOAD SUCCESS")
            print(f"🔗 Image URL: {image_url}")

        except Exception as e:

            print("❌ IMAGE UPLOAD FAILED")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Error: {e}")

            continue


        # -----------------------------
        # 7. SAVE ARTICLE
        # -----------------------------
        print("\n💾 STEP 7: Saving article to Supabase...")

        try:

            result = save_summary_to_db(
                title,
                summary,
                image_url
            )

            print("✅ ARTICLE SAVED TO SUPABASE")
            print(f"📰 {title}")

        except Exception as e:

            print("❌ DATABASE SAVE FAILED")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Error: {e}")

            continue


    # -----------------------------
    # PIPELINE COMPLETE
    # -----------------------------
    print("\n========================================")
    print("🏁 PIPELINE FINISHED")
    print("========================================")

    return render_template(
        'pipeline/run_pipeline.html'
    )
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
