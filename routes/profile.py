from flask import Blueprint, render_template, session, redirect, url_for

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template(
        "profile.html",
        name=session.get("user_name"),
        email=session.get("user_email", "Not Available")
    )