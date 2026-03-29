# interview_agent.py
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the model we found worked for your key!
WORKING_MODEL = "models/gemini-2.5-flash"

def evaluate_answer(question: str, answer: str) -> dict:
    """Evaluate a technical answer using Gemini."""
    
    prompt = f"""
    You are a technical interviewer. Evaluate the candidate's answer to the following question.
    
    Question: {question}
    Candidate's Answer: {answer}
    
    Rate the answer on a scale of 1-10 and provide brief, constructive feedback.
    Return ONLY a JSON object in this format:
    {{
      "score": <number>,
      "feedback": "<string>"
    }}
    """
    
    try:
        model = genai.GenerativeModel(WORKING_MODEL)
        response = model.generate_content(prompt)
        raw = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except Exception as e:
        print(f"Error in interview evaluation: {e}")
        return {
            "score": 0,
            "feedback": "Evaluation failed. Please try again."
        }
