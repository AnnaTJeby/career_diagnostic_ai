from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from resume_parser import extract_text, extract_skills

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

class InterviewRequest(BaseModel):
    question: str
    answer: str

# ── API Endpoints ─────────────────────────────────

@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    """Real implementation for Person 1"""
    content = await file.read()
    text = extract_text(content, file.filename)

    if not text:
        return {"error": "Invalid file format", "extracted_skills": []}

    skills = extract_skills(text)
    return {"extracted_skills": skills}

@app.post("/check-skill-gap")
def check_skill_gap(body: SkillGapRequest):
    # STUB — Person 2 will replace this
    return {
        "job_fit_score": 60,
        "missing_skills": ["Docker", "Statistics"],
        "top_skills_to_learn": ["Docker", "Statistics", "SQL"]
    }

@app.post("/interview")
def interview(body: InterviewRequest):
    # STUB — Person 3 will replace this
    return {"feedback": "Good answer! Expand on scalability.", "score": 7}

@app.get("/health")
def health():
    return {"status": "ok"}
