# utils.py

from textblob import TextBlob
import textstat
import openai
from config import OPENAI_API_KEY
import fitz  # PyMuPDF
from docx import Document

openai.api_key = OPENAI_API_KEY

def analyze_text(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    words = len(blob.words)
    readability = textstat.flesch_reading_ease(text)

    return (
        f"📊 **Analysis Results:**\n"
        f"- Sentiment Score: {sentiment:.2f}\n"
        f"- Word Count: {words}\n"
        f"- Readability Score: {readability:.2f}"
    )

def summarize_text(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Summarize this:\n{text}"}]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"❌ Error summarizing text: {e}"

def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        with fitz.open(file_path) as doc:
            return " ".join(page.get_text() for page in doc)
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        return "Unsupported file type."
