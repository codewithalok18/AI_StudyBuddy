from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

api_configured = False
_config_error = ""

if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        api_configured = True
    except Exception as e:
        _config_error = str(e)
        api_configured = False
else:
    _config_error = "GEMINI_API_KEY not set in environment."

MODEL = "gemini-2.5-flash"

def generate_response(prompt: str) -> str:
    if not api_configured:
        return (
            "❌ Gemini API not configured. "
            "Details: " + _config_error
        )
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text.strip() if response and response.text else "⚠️ No response generated."
    except Exception as e:
        return f"❌ Error generating response: {e}"
