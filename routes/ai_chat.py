from flask import Blueprint, render_template, request
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

ai_chat_bp = Blueprint(
    "ai_chat",
    __name__
)

client = genai.Client(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

@ai_chat_bp.route(
    "/ai-chat",
    methods=["GET", "POST"]
)
def ai_chat():

    question = None
    answer = None

    if request.method == "POST":

        question = request.form.get(
            "question"
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question
        )

        answer = response.text

    return render_template(
        "ai_chat.html",
        question=question,
        answer=answer
    )