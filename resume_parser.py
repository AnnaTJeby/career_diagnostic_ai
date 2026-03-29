import fitz          # PyMuPDF — for PDF
import docx          # python-docx — for DOCX
import json
import io
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def extract_text(file_bytes: bytes, filename: str) -> str:
    """Extract raw text from PDF, DOCX, or TXT file."""
    if filename.lower().endswith(".pdf"):
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        return " ".join(page.get_text() for page in doc)

    elif filename.lower().endswith(".docx"):
        doc = docx.Document(io.BytesIO(file_bytes))
        return " ".join(para.text for para in doc.paragraphs)

    elif filename.lower().endswith(".txt"):
        return file_bytes.decode("utf-8")

    return ""  # unsupported format

def extract_resume_data(text: str) -> dict:
    """Send resume text to Gemini and get back a JSON with name and skills."""
    if not text.strip():
        return {"name": "Candidate", "skills": []}

    prompt = f"""
    Extract the person's full name and all technical skills from this resume text.
    Return ONLY a valid JSON object in this format:
    {{
      "name": "Full Name Here",
      "skills": ["Python", "SQL", "etc"]
    }}
    
    If the name is not found, use "Candidate" for the name.
    No explanation. No markdown. No extra text.

    Resume Text:
    {text[:4000]}
    """
    
    models_to_try = [
        "models/gemini-2.5-flash",
        "models/gemini-1.5-flash",
        "models/gemini-pro"
    ]

    for model_name in models_to_try:
        try:
            current_model = genai.GenerativeModel(model_name)
            response = current_model.generate_content(prompt)
            raw = response.text.strip().replace("```json", "").replace("```", "").strip()
            data = json.loads(raw)
            return {
                "name": data.get("name", "Candidate"),
                "skills": data.get("skills", [])
            }
        except Exception as e:
            print(f"⚠️  {model_name} failed: {e}")
            continue

    return {"name": "Candidate", "skills": []}
