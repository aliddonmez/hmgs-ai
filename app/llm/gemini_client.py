from google import genai
import os
from dotenv import load_dotenv
from retrieval.config import DEBUG_LLM

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY bulunamadı!")

client = genai.Client(api_key=api_key)


def ask_gemini(prompt: str) -> str:
    try:
        if DEBUG_LLM:
            print("DEBUG: Gemini çağrılıyor...")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        if DEBUG_LLM:
            print("DEBUG: Response geldi")

        return response.text

    except Exception as e:
        print("LLM ERROR:", e)
        return "LLM hata verdi."