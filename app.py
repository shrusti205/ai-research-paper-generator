from flask import Flask, render_template, request
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import google.generativeai as genai
import os

app = Flask(__name__)

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


def extract_text(pdf):

    reader = PdfReader(pdf)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


def analyze_paper(text):

    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )

    response = model.generate_content(
        f"""
Analyze this research paper.

SECTION 1:
Create an emoji-rich summary.
Use bullet points.

SECTION 2:
Create exactly 10 flashcards.

Format flashcards EXACTLY:

Q: Question here
A: Answer here

Research Paper:

{text[:3000]}
"""
    )

    return response.text


def parse_response(response_text):

    summary = ""

    flashcards = []

    lines = response_text.split("\n")

    question = None

    flashcard_mode = False

    for line in lines:

        if line.startswith("Q:"):

            flashcard_mode = True

            question = line.replace(
                "Q:",
                ""
            ).strip()

        elif line.startswith("A:") and question:

            answer = line.replace(
                "A:",
                ""
            ).strip()

            flashcards.append({
                "question": question,
                "answer": answer
            })

            question = None

        elif not flashcard_mode:

            summary += line + "\n"

    return summary, flashcards


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        try:

            pdf = request.files["pdf"]

            text = extract_text(pdf)

            result = analyze_paper(text)

            summary, flashcards = parse_response(
                result
            )

            return render_template(
                "result.html",
                summary=summary,
                flashcards=flashcards
            )

        except Exception:

            return render_template(
                "result.html",
                summary="⚠️ Gemini API limit reached. Please try again later.",
                flashcards=[]
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )