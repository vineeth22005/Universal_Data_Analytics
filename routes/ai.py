from flask import Blueprint, render_template, session, redirect, url_for
import pandas as pd

from services.ai_service import generate_ai_insights

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/ai")
def ai():

    if "uploaded_file" not in session:
        return redirect(url_for("upload.upload"))

    filepath = session["uploaded_file"]

    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    summary = f"""

Dataset Name : {session.get("uploaded_filename")}

Total Rows : {df.shape[0]}

Total Columns : {df.shape[1]}

Columns :

{list(df.columns)}

Data Types :

{df.dtypes}

Missing Values :

{df.isnull().sum()}

Duplicate Rows :

{df.duplicated().sum()}

Statistics :

{df.describe(include="all")}

"""

    ai_report = generate_ai_insights(summary)

    return render_template(
        "ai.html",
        ai_report=ai_report
    )