# interview_agent.py
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the model we found worked for your key!
WORKING_MODEL = "models/gemini-2.5-flash"

def generate_initial_question(role: str) -> str:
    """Generate the first interview question for a specific role."""
    prompt = f"You are a technical interviewer for a {role} position. Greet the candidate briefly and ask one initial, high-level technical question to start the interview."
    
    try:
        model = genai.GenerativeModel(WORKING_MODEL)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating initial question: {e}")
        return "Can you tell me about your technical background and some projects you've worked on?"

def evaluate_answer(question: str, answer: str, role: str) -> dict:
    """Evaluate a technical answer and provide the next question."""
    
    prompt = f"""
    You are a technical interviewer for a {role} position. 
    Evaluate the candidate's answer to the following question.
    
    Question: {question}
    Candidate's Answer: {answer}
    
    1. Rate the answer on a scale of 1-10.
    2. Provide brief, constructive feedback.
    3. Ask the NEXT logical technical interview question for a {role} position.
    
    Return ONLY a JSON object in this format:
    {{
      "score": <number>,
      "feedback": "<string>",
      "next_question": "<string>"
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
            "feedback": "Evaluation failed. Please try again.",
            "next_question": "Can you explain another technical concept you're familiar with?"
        }
