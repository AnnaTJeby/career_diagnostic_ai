# skill_gap.py

# Dictionary of roles and their standard required skills
JOB_SKILLS = {
    "data scientist": ["Python", "SQL", "Statistics", "Machine Learning", "TensorFlow", "Docker"],
    "web developer":  ["HTML", "CSS", "JavaScript", "React", "Node.js", "Git", "REST API"],
    "frontend developer": ["React", "TypeScript", "Tailwind CSS", "JavaScript", "UI Design", "Figma"],
    "backend developer":  ["Python", "FastAPI", "PostgreSQL", "Docker", "REST API", "Git", "Redis"],
    "ml engineer":    ["Python", "PyTorch", "TensorFlow", "Scikit-learn", "Docker", "GPU Computing"],
}

def analyze_gap(target_role: str, extracted_skills: list[str]) -> dict:
    # 1. Normalize strings to lowercase for accurate matching
    target_role_clean = target_role.lower().strip()
    required_skills = JOB_SKILLS.get(target_role_clean, [])
    
    if not required_skills:
        # Fallback if the role isn't in our dictionary
        return {
            "job_fit_score": 0,
            "missing_skills": ["Role not found in our database yet!"],
            "top_skills_to_learn": []
        }

    # 2. Perform the Comparison
    have = set(s.lower() for s in extracted_skills)
    need = set(s.lower() for s in required_skills)

    matched = have & need
    missing = [s for s in required_skills if s.lower() not in have]

    # 3. Calculate Score (Percentage)
    score = int((len(matched) / len(need)) * 100) if need else 0

    return {
        "job_fit_score": score,
        "missing_skills": missing,
        "top_skills_to_learn": missing[:3]  # Suggest the first 3 gaps
    }
