# interview_agent.py
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

import random

# Use the model we found worked for your key!
WORKING_MODEL = "models/gemini-2.5-flash"

AI_PERSONAS = ["Sarah", "James", "Alex", "Emily", "Michael", "Sophia", "David", "Jessica"]

def generate_initial_question(role: str, candidate_name: str = "Candidate") -> str:
    """Generate the first interview question with a persona."""
    ai_name = random.choice(AI_PERSONAS)
    prompt = f"""
    You are {ai_name}, a technical interviewer for a {role} position. 
    Greet the candidate as "Candidate".
    Introduce yourself as {ai_name} from the technical team.
    Ask one initial, high-level technical question to start the interview.
    """
    
    try:
        model = genai.GenerativeModel(WORKING_MODEL)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating initial question: {e}")
        return f"Hello {candidate_name}, I'm Sarah. Can you tell me about your technical background?"

def evaluate_answer(question: str, answer: str, role: str, candidate_name: str = "Candidate") -> dict:
    """Evaluate a technical answer and provide the next question."""
    
    prompt = f"""
    You are a technical interviewer for a {role} position. 
    Evaluate their answer to the following question.
    
    Question: {question}
    Candidate's Answer: {answer}
    
    1. Rate the answer on a scale of 1-10.
    2. Provide brief, constructive feedback, addressing them as "Candidate".
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
            "feedback": f"Sorry {candidate_name}, evaluation failed. Please try again.",
            "next_question": "Can you explain another technical concept you're familiar with?"
        }
