from flask import Blueprint, render_template, request, session, redirect, url_for
import pandas as pd

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["GET", "POST"])
def chat():

    if "uploaded_file" not in session:
        return redirect(url_for("upload.upload"))

    filepath = session["uploaded_file"]

    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    answer = ""

    if request.method == "POST":

        question = request.form.get("question", "").lower()

        if "row" in question:
            answer = f"📊 Dataset contains {len(df)} rows."

        elif "column" in question:
            answer = f"📋 Dataset contains {len(df.columns)} columns."

        elif "missing" in question:
            answer = f"⚠ Missing values: {df.isnull().sum().sum()}"

        elif "duplicate" in question:
            answer = f"📄 Duplicate rows: {df.duplicated().sum()}"

        elif "highest" in question or "maximum" in question:

            numeric = df.select_dtypes(include="number").columns

            if len(numeric):
                col = numeric[0]
                answer = f"📈 Highest {col}: {df[col].max()}"
            else:
                answer = "No numeric column found."

        elif "lowest" in question or "minimum" in question:

            numeric = df.select_dtypes(include="number").columns

            if len(numeric):
                col = numeric[0]
                answer = f"📉 Lowest {col}: {df[col].min()}"
            else:
                answer = "No numeric column found."

        elif "average" in question or "mean" in question:

            numeric = df.select_dtypes(include="number").columns

            if len(numeric):
                col = numeric[0]
                answer = f"📊 Average {col}: {round(df[col].mean(), 2)}"
            else:
                answer = "No numeric column found."

        else:
            answer = "🤖 Sorry, I couldn't understand the question."

    return render_template(
        "chat.html",
        answer=answer
    )