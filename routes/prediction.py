from flask import Blueprint, render_template, request, session
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import plotly.express as px

prediction_bp = Blueprint(
    "prediction",
    __name__,
    url_prefix="/prediction"
)

@prediction_bp.route("/", methods=["GET", "POST"])
def prediction():

    print("PREDICTION SESSION:", session)

    uploaded_file = session.get("uploaded_file")

    uploaded_filename = session.get(
        "uploaded_filename",
        session.get("uploaded_file", "No Dataset Uploaded")
    )

    columns = []
    accuracy = None
    target = None
    graph_html = None
    scatter_html = None
    histogram_html = None
    bar_html = None

    # Load dataset from session
    if uploaded_file:

        if uploaded_file.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        columns = df.columns.tolist()

    # Train Model
    if request.method == "POST" and request.form.get("train_model"):

        target = request.form.get("target")

        if uploaded_file:

            if uploaded_file.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            df = df.select_dtypes(include=["number"])

            if target in df.columns:

                X = df.drop(columns=[target])
                y = df[target]

                # Handle missing values
                data = pd.concat([X, y], axis=1)
                data = data.dropna()

                X = data.drop(columns=[target])
                y = data[target]

                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42
                )

                model = LinearRegression()
                model.fit(X_train, y_train)

                predictions = model.predict(X_test)

                fig = px.line(
                    x=range(len(y_test)),
                    y=[y_test.values, predictions],
                    labels={
                        "x": "Test Samples",
                        "value": "Value"
                    }
                )

                fig.update_layout(
                    title="Actual vs Predicted Values"
                )

                def apply_prediction_theme(fig):
                    fig.update_layout(
                        template="plotly_dark",
                        paper_bgcolor="#0B1220",
                        plot_bgcolor="#0B1220",
                        font_color="white",
                        title_font_color="white"
                    )

                    fig.update_xaxes(
                        tickfont=dict(color="white"),
                        title_font=dict(color="white")
                    )

                    fig.update_yaxes(
                        tickfont=dict(color="white"),
                        title_font=dict(color="white"),
                        gridcolor="#1E293B"
                    )

                    return fig

                fig = apply_prediction_theme(fig)
                graph_html = fig.to_html(full_html=False)

                scatter_fig = px.scatter(
                    x=y_test,
                    y=predictions,
                    labels={
                        "x": "Actual Values",
                        "y": "Predicted Values"
                    },
                    title="Actual vs Predicted Scatter Plot"
                )
                scatter_fig = apply_prediction_theme(scatter_fig)
                scatter_html = scatter_fig.to_html(full_html=False)

                hist_fig = px.histogram(
                    x=y,
                    title="Target Column Distribution"
                )

                hist_fig = apply_prediction_theme(hist_fig)

                histogram_html = hist_fig.to_html(full_html=False)


                accuracy = round(
                    r2_score(y_test, predictions) * 100, 2
                )

                bar_fig = px.bar(
                    x=["Actual", "Predicted"],
                    y=[
                        y_test.mean(),
                        predictions.mean()
                    ],
                    title="Average Actual vs Predicted Values"
                )

                bar_fig = apply_prediction_theme(bar_fig)

                bar_html = bar_fig.to_html(full_html=False)


    return render_template(
        "prediction.html",
        columns=columns,
        accuracy=accuracy,
        target=target,
        graph_html=graph_html,
        scatter_html=scatter_html,
        histogram_html=histogram_html,
        bar_html=bar_html,
        uploaded_filename=uploaded_filename
    )