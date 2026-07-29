from flask import Blueprint, render_template, session, request
import pandas as pd
from utils.ai_chat import ask_ai

chat_dataset_bp = Blueprint(
    "chat_dataset",
    __name__
)

@chat_dataset_bp.route("/chat-dataset", methods=["GET", "POST"])
def chat_dataset():

    if "uploaded_file" not in session:
        return "No dataset uploaded."

    filepath = session["uploaded_file"]

    question = None
    answer = None

    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    if request.method == "POST":

        question = request.form.get("question")

        answer = ask_ai(question)

    return render_template(
        "chat_dataset.html",
        rows=df.shape[0],
        columns=df.shape[1],
        question=question,
        answer=answer
    )