import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Searching for Flash models...")
for m in genai.list_models():
    if 'flash' in m.name.lower():
        print(f"Found: {m.name}")
