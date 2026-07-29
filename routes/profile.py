from flask import Blueprint, render_template, session, redirect, url_for, request
import pandas as pd
from werkzeug.utils import secure_filename
import os
from flask import request
profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile")
def profile():


    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    filepath = session.get("uploaded_file")

    total_rows = 0
    total_columns = 0

    if filepath:

        if filepath.endswith(".csv"):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)

        total_rows = len(df)
        total_columns = len(df.columns)

    return render_template(
        "profile.html",
        name=session.get("user_name"),
        email=session.get("user_email", "Not Available"),
        total_rows=total_rows,
        total_columns=total_columns
    )

@profile_bp.route(
    "/upload_profile_image",
    methods=["POST"]
)
def upload_profile_image():

    if "profile_image" not in request.files:
        return redirect(url_for("profile.profile"))

    file = request.files["profile_image"]

    if file.filename == "":
        return redirect(url_for("profile.profile"))

    os.makedirs(
        "static/profile_images",
        exist_ok=True
    )

    filename = secure_filename(file.filename)

    path = os.path.join(
        "static/profile_images",
        filename
    )

    file.save(path)

    session["profile_image"] = filename

    return redirect(
        url_for("profile.profile")
    )