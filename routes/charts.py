from flask import Blueprint, render_template, request, session, redirect, url_for
import pandas as pd
import plotly.express as px
from utils.ai_insights import generate_ai_insights
from utils.ai_recommendations import generate_recommendations

def apply_dark_theme(fig):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0B1220",
        plot_bgcolor="#0B1220",

        xaxis_showline=True,
        yaxis_showline=True,
        font_color="white",

        font=dict(
            color="white",
            size=18
        ),
        xaxis_tickfont=dict(color="white"),
        yaxis_tickfont=dict(color="white"),
        xaxis=dict(color="white"),
        yaxis=dict(color="white"),
        title_font_color="white",
        legend_font_color="white",
        hoverlabel=dict(
            bgcolor="#0B1220",
            font_color="white"
        )
    )
    fig.update_xaxes(
        tickfont=dict(
            color="#FFFFFF",
            size=18
        ),

        title_font=dict(
            color="#FFFFFF",
            size=16
        ),
        showgrid=False,
        tickangle=-30
    )

    fig.update_yaxes(
        tickfont=dict(
            color="#FFFFFF",
            size=18
        ),

        title_font=dict(
            color="#FFFFFF",
            size=16
        ),
        showgrid=True,
        gridcolor="#1E293B"
    )

    fig.update_traces(
        textfont_color="white"
    )


    return fig

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

    ignore_words = [
        "id",
        "code",
        "number",
        "no"
    ]

    columns = [
        col for col in df.columns
        if not any(
            word in col.lower()
            for word in ignore_words
        )
    ]

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    insights = generate_ai_insights(df)
    recommendations = generate_recommendations(df)
    chart_html = None

    if request.method == "POST":

        chart_type = request.form.get("chart_type")
        x = request.form.get("manual_x")
        y = request.form.get("manual_y")

        if chart_type in ["bar", "line", "scatter", "box"] and not y:
            chart_html = """
            <div class='alert alert-warning'>
                Please select a Y Column.
            </div>
            """

            return render_template(
                "charts.html",
                columns=columns,
                numeric_columns=numeric_columns,
                chart=chart_html,
                insights=insights,
                recommendations=recommendations
            )

        try:

            if chart_type == "bar":

                print(chart_type)

                fig = px.bar(
                    df,
                    x=x,
                    y=y
                )



            elif chart_type == "line":

                df_grouped = (
                    df.groupby(x)[y]
                    .mean()
                    .reset_index()
                )

                fig = px.line(
                    df_grouped,
                    x=x,
                    y=y,
                    color_discrete_sequence=["#00FF7F"]
                )

            elif chart_type == "scatter":
                fig = px.scatter(
                    df,
                    x=x,
                    y=y,
                    color_discrete_sequence=["#FFD700"]
                )

            elif chart_type == "pie":
                fig = px.pie(
                    df,
                    names=x,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )

            elif chart_type == "histogram":
                fig = px.histogram(
                    df,
                    x=x,
                    color_discrete_sequence=["#636EFA"]
                )



            else:
                fig = px.bar(df, x=x, y=y)

            fig = apply_dark_theme(fig)

            if chart_type in ["bar", "histogram"]:
                fig.update_traces(
                    marker_color="#636EFA"
                )

            chart_html = fig.to_html(full_html=False)

        except Exception as e:

            chart_html = (
                f"<div class='alert alert-danger'>{e}</div>"
            )

    return render_template(
        "charts.html",
        columns=columns,
        numeric_columns=numeric_columns,
        chart=chart_html,
        insights=insights,
        recommendations=recommendations,
        selected_x=x if 'x' in locals() else "",
        selected_y=y if 'y' in locals() else ""
    )
