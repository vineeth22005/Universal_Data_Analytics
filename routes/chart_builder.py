from flask import Blueprint, render_template, request, session, redirect, url_for
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

chart_builder_bp = Blueprint("chart_builder", __name__)


@chart_builder_bp.route("/chart-builder", methods=["GET", "POST"])
def chart_builder():

    if "uploaded_file" not in session:
        return redirect(url_for("upload.upload"))

    filepath = session["uploaded_file"]

    try:
        if filepath.endswith(".csv"):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)

    except Exception as e:
        return f"Error loading dataset: {e}"

    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    categorical_columns = (
        df.select_dtypes(include=["object", "category"])
        .columns
        .tolist()
    )

    chart_html = None

    if request.method == "POST":

        x_column = request.form.get("x_column")
        y_column = request.form.get("y_column")
        chart_type = request.form.get("chart_type")

        # Auto Recommend
        if not chart_type or chart_type == "Auto":

            if x_column and y_column:
                chart_type = "Bar"

            elif y_column:
                chart_type = "Histogram"

            else:
                chart_type = "Scatter"

        try:

            if chart_type == "Bar":

                fig = px.bar(
                    df,
                    x=x_column,
                    y=y_column,
                    title=f"{y_column} by {x_column}"
                )

            elif chart_type == "Line":

                fig = px.line(
                    df,
                    x=x_column,
                    y=y_column,
                    title=f"{y_column} by {x_column}"
                )

            elif chart_type == "Scatter":

                fig = px.scatter(
                    df,
                    x=x_column,
                    y=y_column,
                    title=f"{y_column} vs {x_column}"
                )

            elif chart_type == "Histogram":

                fig = px.histogram(
                    df,
                    x=y_column,
                    title=f"Distribution of {y_column}"
                )

            elif chart_type == "Pie":

                pie_data = (
                    df.groupby(x_column)[y_column]
                    .sum()
                    .reset_index()
                )

                fig = px.pie(
                    pie_data,
                    names=x_column,
                    values=y_column,
                    title=f"{y_column} Distribution"
                )

            elif chart_type == "Box":

                fig = px.box(
                    df,
                    x=x_column,
                    y=y_column,
                    title=f"{y_column} Box Plot"
                )

            elif chart_type == "Area":

                fig = px.area(
                    df,
                    x=x_column,
                    y=y_column,
                    title=f"{y_column} Area Chart"
                )

            elif chart_type == "Heatmap":

                corr = df.select_dtypes(include="number").corr()

                fig = go.Figure(
                    data=go.Heatmap(
                        z=corr.values,
                        x=corr.columns,
                        y=corr.columns,
                        colorscale="Viridis",
                        text=corr.round(2).values,
                        texttemplate="%{text}"
                    )
                )

                fig.update_layout(
                    title="Correlation Heatmap"
                )

            else:

                fig = px.bar(
                    df,
                    x=x_column,
                    y=y_column
                )

            fig.update_layout(
                template="plotly_dark",
                height=600,
                title_x=0.5,
                font=dict(size=14)
            )

            chart_html = fig.to_html(
                full_html=False,
                include_plotlyjs="cdn"
            )

        except Exception as e:

            chart_html = f"""
            <div class='alert alert-danger'>
                Error generating chart:<br>
                {str(e)}
            </div>
            """

    return render_template(
        "chart_builder.html",
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        chart_html=chart_html
    )