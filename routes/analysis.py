from flask import Blueprint, render_template, session, redirect, url_for
import pandas as pd

analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.route("/analysis")
def analysis():

    if "uploaded_file" not in session:
        return redirect(url_for("upload.upload"))

    filepath = session["uploaded_file"]

    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    summary = df.describe(include="all").to_html(
        classes="table table-bordered",
        index=True
    )

    return render_template(
        "analysis.html",
        summary=summary
    )