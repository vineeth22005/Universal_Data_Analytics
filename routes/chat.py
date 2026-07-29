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

            for col in df.select_dtypes(include="number").columns:

                if col.lower() in question:
                    answer = f"📈 Highest {col}: {df[col].max()}"
                    break

            else:
                answer = "Please mention a column name."

        elif "lowest" in question or "minimum" in question:

            for col in df.select_dtypes(include="number").columns:

                if col.lower() in question:
                    answer = f"📉 Lowest {col}: {df[col].min()}"
                    break

            else:
                answer = "Please mention a column name."

        elif "average" in question or "mean" in question:

            for col in df.select_dtypes(include="number").columns:

                if col.lower() in question:
                    answer = (
                        f"📊 Average {col}: "
                        f"{round(df[col].mean(), 2)}"
                    )
                    break

            else:
                answer = "Please mention a column name."



        else:
            answer = "🤖 Sorry, I couldn't understand the question."

    return render_template(
        "chat.html",
        answer=answer
    )