from flask import Blueprint, render_template, session, redirect, url_for
import pandas as pd
import plotly.express as px

ai_dashboard_bp = Blueprint("ai_dashboard", __name__)


@ai_dashboard_bp.route("/ai-dashboard")
def ai_dashboard():

    if "uploaded_file" not in session:
        return redirect(url_for("upload.upload"))

    filepath = session["uploaded_file"]

    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    charts = []

    try:

        # Bar Chart
        if categorical_cols and numeric_cols:
            fig = px.bar(
                df,
                x=categorical_cols[0],
                y=numeric_cols[0],
                title=f"{numeric_cols[0]} by {categorical_cols[0]}"
            )
            charts.append(fig.to_html(full_html=False))

        # Pie Chart
        if categorical_cols:
            fig = px.pie(
                df,
                names=categorical_cols[0],
                title=f"{categorical_cols[0]} Distribution"
            )
            charts.append(fig.to_html(full_html=False))

        # Histogram
        if numeric_cols:
            fig = px.histogram(
                df,
                x=numeric_cols[0],
                title=f"{numeric_cols[0]} Distribution"
            )
            charts.append(fig.to_html(full_html=False))

        # Scatter Plot
        if len(numeric_cols) >= 2:
            fig = px.scatter(
                df,
                x=numeric_cols[0],
                y=numeric_cols[1],
                title=f"{numeric_cols[0]} vs {numeric_cols[1]}"
            )
            charts.append(fig.to_html(full_html=False))

    except Exception as e:
        print(e)

    return render_template(
        "ai_dashboard.html",
        charts=charts
    )