import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_ai_insights(summary_text):

    prompt = f"""
You are a Senior Data Analyst.

Analyze this dataset.

{summary_text}

Provide:

1. Dataset Overview
2. Data Quality
3. Missing Values
4. Interesting Patterns
5. Business Insights
6. Recommendations

Answer professionally in simple English.
"""

    retries = 3

    for attempt in range(retries):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error = str(e)

            if "503" in error:

                if attempt < retries - 1:
                    time.sleep(5)
                    continue

                return (
                    "⚠️ Gemini AI is currently busy.\n\n"
                    "Please wait a few minutes and try again."
                )

            return f"AI Error: {error}"

    return "AI service is unavailable."