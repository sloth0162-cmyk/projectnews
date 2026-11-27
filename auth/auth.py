from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    session,
)

import requests

from config import Config

auth_bp = Blueprint("auth", __name__)
# -----------------------------
# Google Auth (Supabase)
# -----------------------------
@auth_bp.route("/auth/login")
def login_google():
    callback_url = url_for("auth.auth_callback", _external=True)

    return redirect(
        f"{Config.SUPABASE_URL}/auth/v1/authorize"
        f"?provider=google&redirect_to={callback_url}"
    )


@auth_bp.route("/auth/callback", methods=["GET", "POST"])
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
         "access_token": access_token,
    }

    return redirect("/")


@auth_bp.route("/auth/me", methods=["GET"])
def auth_me():
    user = session.get("user")

    if not user:
        return jsonify({
            "logged_in": False
        }), 200

    metadata = user.get("user_metadata") or {}

    name = (
        metadata.get("full_name")
        or metadata.get("name")
        or metadata.get("given_name")
        or "Subscriber"
    )

    avatar = (
        metadata.get("avatar_url")
        or metadata.get("picture")
        or "https://cdn-icons-png.flaticon.com/512/847/847969.png"
    )

    return jsonify({
        "logged_in": True,
        "user": {
            "id": user.get("id"),
            "email": user.get("email"),
            "name": name,
            "avatar": avatar
        }
    })

# -----------------------------
# Logoutroute
# -----------------------------
@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")
# -----------------------------
# Subscriber Page
# -----------------------------
@auth_bp.route("/subscriber")
def subscriber_page():
    if session.get("user"):
        return redirect(url_for("auth.profile_page"))

    return render_template("subscriber.html")
# -----------------------------
# Profile
# -----------------------------

@auth_bp.route("/profile", methods=["GET", "POST"])
def profile_page():
    user = session.get("user")

    if not user:
        return redirect(url_for("auth.login_google"))

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
            display_name = " ".join(
                filter(None, [first_name, last_name])
            )

            access_token = user.get("access_token")

            if not access_token:
                notice = "Your session has expired. Please sign in again."

            else:
                updated_metadata = {
                    **metadata,
                    "given_name": first_name,
                    "family_name": last_name,
                    "full_name": display_name,
                    "name": display_name,
                }

                try:
                    response = requests.put(
                        f"{Config.SUPABASE_URL}/auth/v1/user",
                        headers={
                            "apikey": Config.SUPABASE_KEY,
                            "Authorization": f"Bearer {access_token}",
                            "Content-Type": "application/json",
                        },
                        json={"data": updated_metadata},
                        timeout=10,
                    )

                    if response.ok:
                        updated_user = response.json()

                        user["user_metadata"] = (
                            updated_user.get("user_metadata")
                            or updated_metadata
                        )

                        session["user"] = user
                        session["profile_notice"] = (
                            "Your profile name was updated successfully."
                        )

                        return redirect(url_for("auth.profile_page"))

                    print("Profile update failed:", response.text)
                    notice = "Unable to update your profile. Please try again."

                except requests.RequestException as error:
                    print("Profile update error:", error)
                    notice = "Could not connect to the account service."

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
        last_name = last_name or (
            parts[1] if len(parts) > 1 else ""
        )

    first_name = first_name or "New"
    last_name = last_name or ("Sloth" if not full_name else "")

    display_name = " ".join(
        filter(None, [first_name, last_name])
    )

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
    )
