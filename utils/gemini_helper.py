"""
StudyBuddy AI
Author: Alok Kumar
Description: AI-powered study assistant built with Streamlit & Gemini
"""


import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env locally (Streamlit Cloud ignores this and uses Secrets)
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "models/gemini-2.5-flash"

def generate_response(prompt: str) -> str:
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini error: {e}"
