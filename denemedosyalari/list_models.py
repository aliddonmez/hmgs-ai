# analysis/list_models.py
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

print("--- MODELLER ---")
try:
    # Hiçbir filtreleme yapmadan direkt ne varsa yazdıralım
    for m in client.models.list():
        # m nesnesinin "name" özelliği genellikle vardır
        print(f"- {m.name}")
except Exception as e:
    print(f"Hata: {e}")