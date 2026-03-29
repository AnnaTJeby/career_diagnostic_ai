import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 Searching for a working model...")

working_model = None

for m in genai.list_models():
    # Only try models that support generation and have basic Flash/Pro names
    if 'generateContent' in m.supported_generation_methods:
        name = m.name
        print(f"Testing {name}...")
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content("Hi", request_options={"timeout": 5})
            print(f"✅ SUCCESS: {name}")
            working_model = name
            break
        except Exception as e:
            print(f"❌ FAILED: {name}")

with open("working_model.txt", "w") as f:
    if working_model:
        f.write(working_model)
        print(f"\n✨ FOUND IT: {working_model}")
    else:
        f.write("NONE")
        print("\n💀 NONE FOUND.")
