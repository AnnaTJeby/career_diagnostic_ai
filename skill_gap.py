import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def analyze_gap(target_role: str, extracted_skills: list[str], degree: str = "Not specified", interests: str = "Not specified") -> dict:
    """Use Gemini to perform a deep skill gap analysis and generate a project roadmap."""
    
    prompt = f"""
    You are a career diagnostic engine. 
    Analyze the gap between a candidate's current skills and a target role.
    
    Candidate Profile:
    - Target Role: {target_role}
    - Current Skills: {", ".join(extracted_skills)}
    - Degree: {degree}
    - Interests: {interests}
    
    Provide a detailed analysis in JSON format:
    1. "job_fit_score": A number (0-100) representing how well the current skills match the target role.
    2. "missing_skills": A list of key technical skills needed for the role that are missing from their current skills.
    3. "top_skills_to_learn": The most critical 3 skills they should focus on next.
    4. "project_roadmap": A 3-step personalized project roadmap to help them bridge the gap and build their portfolio.
    
    Return ONLY a valid JSON object. No extra text.
    """

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)
        return data
    except Exception as e:
        print(f"Error in LLM gap analysis: {e}")
        # Fallback to a safer response if the LLM fails
        return {
            "job_fit_score": 0,
            "missing_skills": ["Analysis temporarily unavailable"],
            "top_skills_to_learn": ["Check back soon"],
            "project_roadmap": ["Step 1: Continue learning", "Step 2: Build projects", "Step 3: Network"]
        }
