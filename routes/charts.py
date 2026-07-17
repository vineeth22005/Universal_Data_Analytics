from flask import Blueprint, render_template, request, session, redirect, url_for
import pandas as pd
import plotly.express as px
from utils.chart_recommender import recommend_chart
from utils.ai_insights import generate_ai_insights
from utils.ai_recommendations import generate_recommendations

charts_bp = Blueprint("charts", __name__)


@charts_bp.route("/charts", methods=["GET", "POST"])
def charts():

    if "uploaded_file" not in session:
        return redirect(url_for("upload.upload"))

    filepath = session["uploaded_file"]

    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    columns = df.columns.tolist()
    insights = generate_ai_insights(df)
    recommendations = generate_recommendations(df)

    recommendation = recommend_chart(df)

    auto_chart = recommendation.get("chart")
    auto_x = recommendation.get("x")
    auto_y = recommendation.get("y")

    charts = []
    chart_html = None
    ai_chart_html = None

    manual_chart_html = None

    try:

        if auto_chart == "bar":
            fig = px.bar(df, x=auto_x, y=auto_y)

        elif auto_chart == "line":
            fig = px.line(df, x=auto_x, y=auto_y)

        elif auto_chart == "scatter":
            fig = px.scatter(df, x=auto_x, y=auto_y)

        elif auto_chart == "histogram":
            fig = px.histogram(df, x=auto_x)

        elif auto_chart == "pie":
            fig = px.pie(df, names=auto_x)

        else:
            fig = None

        if fig:
            chart_html = fig.to_html(full_html=False)

    except Exception:
        pass

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    try:

        # Bar Chart

        if len(categorical_cols) > 0 and len(numeric_cols) > 0:
            bar_df = (
                df.groupby(categorical_cols[0])[numeric_cols[0]]
                .sum()
                .reset_index()
                .sort_values(numeric_cols[0], ascending=False)
                .head(10)
            )

            fig = px.bar(
                bar_df,
                x=categorical_cols[0],
                y=numeric_cols[0],
                title="Top 10 " + categorical_cols[0]
            )

            charts.append(fig.to_html(full_html=False))

        # Pie Chart

        if len(categorical_cols) > 0:
            pie_df = (
                df[categorical_cols[0]]
                .value_counts()
                .head(10)
                .reset_index()
            )

            pie_df.columns = [categorical_cols[0], "Count"]

            fig = px.pie(
                pie_df,
                names=categorical_cols[0],
                values="Count",
                title="Top 10 " + categorical_cols[0]
            )

            charts.append(fig.to_html(full_html=False))

        # Histogram

        if len(numeric_cols) > 0:
            fig = px.histogram(
                df,
                x=numeric_cols[0],
                nbins=30,
                title=numeric_cols[0] + " Distribution"
            )

            charts.append(fig.to_html(full_html=False))

        # Box Plot

        if len(numeric_cols) > 0:
            fig = px.box(
                df,
                y=numeric_cols[0],
                title=numeric_cols[0] + " Box Plot"
            )

            charts.append(fig.to_html(full_html=False))

    except Exception as e:

        print(e)

    if request.method == "POST":

        mode = request.form.get("mode")

        if mode == "manual":

            chart_type = request.form.get("chart_type")
            x = request.form.get("manual_x")
            y = request.form.get("manual_y")

        else:

            x = request.form.get("x_column")
            y = request.form.get("y_column")

        try:

            x_is_numeric = pd.api.types.is_numeric_dtype(df[x])

            y_is_numeric = False

            if y:
                y_is_numeric = pd.api.types.is_numeric_dtype(df[y])

            # ==========================
            # MANUAL CHART MODE
            # ==========================

            if mode == "manual":

                if chart_type == "bar":
                    fig = px.bar(df, x=x, y=y)

                elif chart_type == "line":
                    fig = px.line(df, x=x, y=y)

                elif chart_type == "scatter":
                    fig = px.scatter(df, x=x, y=y)

                elif chart_type == "pie":
                    fig = px.pie(df, names=x)

                elif chart_type == "histogram":
                    fig = px.histogram(df, x=x)

                elif chart_type == "box":
                    fig = px.box(df, y=y)

                else:
                    fig = px.bar(df, x=x, y=y)

            # ==========================
            # AI SMART CHART MODE
            # ==========================

            else:

                if y and (not x_is_numeric) and y_is_numeric:

                    fig = px.bar(df, x=x, y=y)

                elif y and x_is_numeric and y_is_numeric:

                    fig = px.scatter(df, x=x, y=y)

                elif y and pd.api.types.is_datetime64_any_dtype(df[x]):

                    fig = px.line(df, x=x, y=y)

                elif not y and (not x_is_numeric):

                    fig = px.pie(df, names=x)

                elif not y and x_is_numeric:

                    fig = px.histogram(df, x=x)

                else:

                    fig = px.bar(df, x=x, y=y)

            chart_html = fig.to_html(full_html=False)

        except Exception as e:

            chart_html = f"<div class='alert alert-danger'>{e}</div>"

    return render_template(
        "charts.html",
        columns=columns,
        charts=charts,
        chart=chart_html,
        auto_chart=auto_chart,
        auto_x=auto_x,
        auto_y=auto_y,
        insights=insights,
        recommendations=recommendations
    )
