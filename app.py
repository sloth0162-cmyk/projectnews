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
import time
import os

# -----------------------------
# 🔧 Flask App Setup
# -----------------------------
app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

PIPELINE_PASSWORD = Config.PIPELINE_PASSWORD
app.register_blueprint(article_bp)
app.register_blueprint(second, url_prefix="/secondpage")


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
        query = query.contains("tags", [tag])

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


    return render_template(
        "dashboard.html",
        articles=articles,
        finance_articles=finance_articles,
        current_tag=tag or "All",
        search_query=search,
    )

#about
# -----------------------------
# 📄 About Page
# -----------------------------
@app.route("/about")
def about_page():
    return render_template("secondpage/about.html")



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
# Google Auth (Supabase)
# -----------------------------
@app.route("/auth/login")
def login_google():
    callback_url = url_for("auth_callback", _external=True)

    return redirect(
        f"{Config.SUPABASE_URL}/auth/v1/authorize"
        f"?provider=google&redirect_to={callback_url}"
    )


@app.route("/auth/callback", methods=["GET", "POST"])
def auth_callback():
    access_token = (
        request.form.get("access_token")
        or request.args.get("access_token")
    )

    # Read the access token from the URL fragment.
    if not access_token:
        return """
        <p>Signing you in...</p>
        <script>
            const token = new URLSearchParams(
                window.location.hash.slice(1)
            ).get("access_token");

            if (token) {
                const form = document.createElement("form");
                form.method = "POST";
                form.action = "/auth/callback";

                const input = document.createElement("input");
                input.type = "hidden";
                input.name = "access_token";
                input.value = token;

                form.appendChild(input);
                document.body.appendChild(form);
                form.submit();
            } else {
                window.location.replace("/");
            }
        </script>
        """

    # Verify the user with Supabase.
    response = requests.get(
        f"{Config.SUPABASE_URL}/auth/v1/user",
        headers={
            "apikey": Config.SUPABASE_KEY,
            "Authorization": f"Bearer {access_token}",
        },
        timeout=10,
    )

    if not response.ok:
        print("Login failed:", response.text)
        return redirect("/")

    user = response.json()

    session["user"] = {
        "id": user.get("id"),
        "email": user.get("email"),
        "user_metadata": user.get("user_metadata") or {},
    }

    return redirect(url_for("dashboard_page"))


# -----------------------------
# Profile
# -----------------------------
@app.route("/profile", methods=["GET", "POST"])
def profile_page():
    user = session.get("user")

    if not user:
        return redirect(url_for("login_google"))

    metadata = user.get("user_metadata") or {}
    notice = session.pop("profile_notice", None)

    # Update the user's display name.
    if request.method == "POST" and request.form.get("action") == "update_name":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()

        if not first_name:
            notice = "Please enter your first name."
        elif len(first_name) > 60 or len(last_name) > 60:
            notice = "Names must be 60 characters or fewer."
        else:
            display_name = " ".join(filter(None, [first_name, last_name]))

            metadata.update({
                "given_name": first_name,
                "family_name": last_name,
                "full_name": display_name,
                "name": display_name,
            })

            user["user_metadata"] = metadata
            session["user"] = user
            session["profile_notice"] = "Your name was updated for this session."

            return redirect(url_for("profile_page"))

    # Get the user's name.
    full_name = (
        metadata.get("full_name")
        or metadata.get("name")
        or user.get("name")
        or ""
    ).strip()

    first_name = (metadata.get("given_name") or "").strip()
    last_name = (metadata.get("family_name") or "").strip()

    if not first_name and full_name:
        parts = full_name.split(maxsplit=1)
        first_name = parts[0]
        last_name = last_name or (parts[1] if len(parts) > 1 else "")

    first_name = first_name or "New"
    last_name = last_name or ("Sloth" if not full_name else "")

    display_name = " ".join(filter(None, [first_name, last_name]))

    # Get the user's profile picture.
    avatar_url = (
        metadata.get("avatar_url")
        or metadata.get("picture")
        or "https://cdn-icons-png.flaticon.com/512/847/847969.png"
    )

    return render_template(
        "profile.html",
        first_name=first_name,
        last_name=last_name,
        display_name=display_name,
        avatar_url=avatar_url,
        saved_articles=[],
        notice=notice,
    )# -----------------------------
# ⚙️ Run News Pipeline (General)
# Replace the existing _pipeline_respond + run_pipeline block with this.
# app.py must have `import os` and `import time` at the top.
# -----------------------------

_SENSITIVE_ENV_HINTS = ("KEY", "TOKEN", "SECRET", "PASSWORD", "PASS", "SUPABASE", "DATABASE")


def _redact(value, limit=500):
    """Make text safe for the JSON response: mask secret values, cap length."""
    text = str(value)

    secrets = [PIPELINE_PASSWORD]
    for name, env_value in os.environ.items():
        if any(hint in name.upper() for hint in _SENSITIVE_ENV_HINTS):
            secrets.append(env_value)

    for secret in secrets:
        if secret and len(secret) >= 4:
            text = text.replace(secret, "[REDACTED]")

    return text if len(text) <= limit else text[:limit] + "…"


def _pipeline_stats(debug_log, fetched, saved, start_time):
    article_entries = [e for e in debug_log if e["step"].startswith("article[")]
    return {
        "articles_fetched": fetched,
        "articles_saved": saved,
        "skipped": sum(1 for e in article_entries if e["status"] == "skipped"),
        "failed": sum(1 for e in article_entries if e["status"] == "failed"),
        "warnings": sum(1 for e in debug_log if e["status"] == "warning"),
        "total_elapsed_s": round(time.monotonic() - start_time, 2),
    }


def _pipeline_respond(debug_log, error=None, status_code=None, stats=None):
    """?debug=1 returns raw JSON for easier debugging."""

    if status_code is None:
        status_code = 500 if error else 200

    if request.args.get("debug") == "1":
        payload = {
            "error": error,
            "log": debug_log
        }
        if stats is not None:
            payload["stats"] = stats
        return jsonify(payload), status_code

    return render_template(
        "pipeline/run_pipeline.html",
        error=error,
        debug_log=debug_log,
    ), status_code


@app.route("/run_pipeline", methods=["GET", "POST"])
def run_pipeline():

    # -----------------------------
    # GET → Show pipeline page
    # -----------------------------
    if request.method == "GET":
        return render_template(
            "pipeline/run_pipeline.html"
        )

    # -----------------------------
    # Check password (unchanged check; response now 401 + JSON in debug mode)
    # -----------------------------
    password = request.form.get("password")

    if password != PIPELINE_PASSWORD:
        print("❌ Pipeline rejected: Incorrect password")

        return _pipeline_respond(
            [],
            error="Incorrect password",
            status_code=401
        )

    start_time = time.monotonic()
    debug_log = []
    fetched = 0

    def log_step(step, status, detail=""):
        debug_log.append({
            "step": step,
            "status": status,
            "detail": _redact(detail),
            "elapsed_s": round(
                time.monotonic() - start_time,
                2
            ),
        })

        print(f"[{status}] {step}: {detail}")

    log_step("pipeline", "start")

    # -----------------------------
    # 1. SCRAPE NEWS
    # -----------------------------
    log_step("scrape", "start")

    try:
        articles = scrape_news()

        scraper_errors = getattr(
            scrape_news,
            "last_errors",
            []
        )

        if scraper_errors:
            log_step(
                "scrape",
                "warning",
                f"{len(scraper_errors)} feed error(s)"
            )
            # One entry per failing feed (capped) so each can be identified.
            for feed_error in list(scraper_errors)[:10]:
                log_step("scrape.feed", "warning", feed_error)

        fetched = len(articles) if articles else 0

        log_step(
            "scrape",
            "ok",
            f"{fetched} article(s) fetched"
        )

    except Exception as e:
        log_step(
            "scrape",
            "failed",
            f"{type(e).__name__}: {e}"
        )

        return _pipeline_respond(
            debug_log,
            error=_redact(f"Scraper failed: {e}"),
            stats=_pipeline_stats(debug_log, fetched, 0, start_time)
        )

    if not articles:
        log_step(
            "scrape",
            "failed",
            "0 articles returned"
        )

        return _pipeline_respond(
            debug_log,
            error="No articles were returned by the scraper.",
            stats=_pipeline_stats(debug_log, fetched, 0, start_time)
        )

    # -----------------------------
    # 2. PROCESS ARTICLES
    # -----------------------------
    processed = 0

    for index, article in enumerate(
        articles,
        start=1
    ):
        # Any unexpected exception is recorded and the loop moves on,
        # so the debug log can still be returned to the browser.
        try:

            # `or ""` guards against None values (previously an AttributeError).
            title = (article.get("title") or "").strip()
            content = (article.get("content") or "").strip()
            source = article.get("source") or "Unknown"
            url = article.get("url") or "Unknown"

            if not title:
                log_step(
                    f"article[{index}]",
                    "skipped",
                    "no title"
                )
                continue

            if not content:
                log_step(
                    f"article[{index}]",
                    "skipped",
                    "no content"
                )
                continue

            log_step(
                f"article[{index}]",
                "start",
                f"{source}: {title}"
            )

            # -----------------------------
            # 3. CHECK SUPABASE
            # -----------------------------
            try:
                exists = (
                    supabase
                    .table("articles")
                    .select("id")
                    .eq("title", title)
                    .execute()
                )

                matches = exists.data or []

            except Exception as e:
                log_step(
                    f"article[{index}]",
                    "failed",
                    f"dup-check error: "
                    f"{type(e).__name__}: {e}"
                )
                continue

            if matches:
                log_step(
                    f"article[{index}]",
                    "skipped",
                    f"duplicate: {title}"
                )
                continue

            # -----------------------------
            # 4. SUMMARIZE
            # -----------------------------
            try:
                summary = summarize_text(content)

                if not summary:
                    log_step(
                        f"article[{index}]",
                        "failed",
                        "summarizer returned empty result"
                    )
                    continue

            except Exception as e:
                log_step(
                    f"article[{index}]",
                    "failed",
                    f"summarizer error: "
                    f"{type(e).__name__}: {e}"
                )
                continue

            # -----------------------------
            # 5. GENERATE IMAGE (returns image bytes, nothing saved locally)
            # -----------------------------
            try:
                image_bytes = create_news_image(
                    title,
                    summary
                )

                if not image_bytes:
                    log_step(
                        f"article[{index}]",
                        "failed",
                        "image generation returned empty result"
                    )
                    continue

                if not isinstance(image_bytes, (bytes, bytearray)):
                    log_step(
                        f"article[{index}]",
                        "failed",
                        f"image generation returned "
                        f"{type(image_bytes).__name__}, expected bytes"
                    )
                    continue

            except Exception as e:
                log_step(
                    f"article[{index}]",
                    "failed",
                    f"image-gen error: "
                    f"{type(e).__name__}: {e}"
                )
                continue

            # -----------------------------
            # 6. UPLOAD IMAGE (bytes → Supabase Storage)
            # -----------------------------
            try:
                image_url = upload_image(
                    image_bytes
                )

                if not image_url:
                    log_step(
                        f"article[{index}]",
                        "failed",
                        "image upload returned empty result"
                    )
                    continue

            except Exception as e:
                log_step(
                    f"article[{index}]",
                    "failed",
                    f"image-upload error: "
                    f"{type(e).__name__}: {e}"
                )
                continue

            # -----------------------------
            # 7. SAVE ARTICLE
            # -----------------------------
            try:
                save_summary_to_db(
                    title,
                    summary,
                    image_url
                )

                processed += 1

                log_step(
                    f"article[{index}]",
                    "ok",
                    f"saved: {title}"
                )

            except Exception as e:
                log_step(
                    f"article[{index}]",
                    "failed",
                    f"db-save error: "
                    f"{type(e).__name__}: {e}"
                )
                continue

            # -----------------------------
            # 8. CLASSIFY ARTICLE
            # -----------------------------
            try:
                tags = classify_article(title, summary)

                save_tags_to_article(title, tags)

                if tags:
                    log_step(
                        f"article[{index}]",
                        "ok",
                        f"tags saved: {tags}"
                    )
                else:
                    log_step(
                        f"article[{index}]",
                        "warning",
                        "classifier returned no tags (save was still attempted)"
                    )

            except Exception as e:
                log_step(
                    f"article[{index}]",
                    "warning",
                    f"tagging error: {type(e).__name__}: {e}"
                )

        except Exception as e:
            log_step(
                f"article[{index}]",
                "failed",
                f"unexpected error: {type(e).__name__}: {e}"
            )
            continue

    # -----------------------------
    # PIPELINE COMPLETE
    # -----------------------------
    total_elapsed = round(
        time.monotonic() - start_time,
        2
    )

    log_step(
        "pipeline",
        "finished",
        f"{processed} saved, "
        f"{total_elapsed}s total"
    )

    return _pipeline_respond(
        debug_log,
        stats=_pipeline_stats(debug_log, fetched, processed, start_time)
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
    """Sloth Newz Finance."""
    try:
        result = (
            supabase.table("finance_articles")
            .select("*")
            .order("id", desc=True)
            .execute()
        )

        articles = result.data or []

        print("FINANCE ARTICLES:")
        print(articles)

    except Exception as e:
        print("⚠️ Error fetching finance articles:", e)
        articles = []

    return render_template(
        "finance/index.html",
        articles=articles
    )

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