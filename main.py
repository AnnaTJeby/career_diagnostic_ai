from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from skill_gap import analyze_gap
from resume_parser import extract_text, extract_resume_data
from interview_agent import evaluate_answer, generate_initial_question

app = FastAPI()

# ✅ REQUIRED — allows your frontend to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Schemas ───────────────────────────────────────
class SkillGapRequest(BaseModel):
    target_role: str
    extracted_skills: List[str]

class StartInterviewRequest(BaseModel):
    role: str
    candidate_name: str = "Candidate"

class InterviewRequest(BaseModel):
    role: str
    question: str
    answer: str
    candidate_name: str = "Candidate"

# ── API Endpoints ─────────────────────────────────

@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    """Extract name and skills from resume."""
    content = await file.read()
    text = extract_text(content, file.filename)

    if not text:
        return {"error": "Invalid file format", "name": "Candidate", "extracted_skills": []}

    data = extract_resume_data(text)
    return {
        "name": data.get("name", "Candidate"),
        "extracted_skills": data.get("skills", [])
    }

@app.post("/check-skill-gap")
def check_skill_gap(body: SkillGapRequest):
    result = analyze_gap(body.target_role, body.extracted_skills)
    return result

@app.post("/interview-start")
def interview_start(body: StartInterviewRequest):
    """Generate the first question with a persona."""
    question = generate_initial_question(body.role, body.candidate_name)
    return {"question": question}

@app.post("/interview")
def interview(body: InterviewRequest):
    """Evaluate and get next question."""
    result = evaluate_answer(body.question, body.answer, body.role, body.candidate_name)
    return result

@app.get("/health")
def health():
    return {"status": "ok"}
