from flask import Blueprint, render_template, request, session
import pandas as pd

from services.ai_service import generate_ai_insights

ai_chat_bp = Blueprint("ai_chat", __name__)


@ai_chat_bp.route("/ai-chat", methods=["GET", "POST"])
def ai_chat():

    response = ""

    if request.method == "POST":

        question = request.form.get("question")

        if "uploaded_file" in session:

            filepath = session["uploaded_file"]

            if filepath.endswith(".csv"):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)

            preview = df.head(20).to_string(index=False)

            dataset = f"""
            You are an expert Data Analyst.

            Analyze the uploaded dataset and answer ONLY based on the data provided.

            Dataset Summary
            ----------------
            Rows : {df.shape[0]}
            Columns : {df.shape[1]}

            Column Names:
            {list(df.columns)}

            Data Types:
            {df.dtypes.to_string()}

            Missing Values:
            {df.isnull().sum().to_string()}

            Statistics:
            {df.describe(include='all').to_string()}

            Dataset Preview (First 20 Rows)
            --------------------------------
            {preview}

            User Question:
            {question}
            """

            response = generate_ai_insights(dataset)

        else:
            response = "Please upload a dataset first."

    return render_template(
        "ai_chat.html",
        response=response
    )