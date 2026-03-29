import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 Searching for a working model...")

working_model = None

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"Testing {m.name}...", end=" ", flush=True)
        try:
            model = genai.GenerativeModel(m.name)
            response = model.generate_content("Hi", request_options={"timeout": 5})
            print("✅ WORKING!")
            working_model = m.name
            break
        except Exception as e:
            err = str(e)
            if "429" in err:
                print("❌ 429 (Quota)")
            elif "404" in err:
                print("❌ 404 (Not Found)")
            else:
                print(f"❌ Error: {err[:50]}...")

if working_model:
    print(f"\n✨ FOUND IT! Use this model: {working_model}")
else:
    print("\n💀 No working models found. Check your API key at aistudio.google.com")
