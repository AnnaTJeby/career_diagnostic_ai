from resume_parser import extract_text, extract_skills

print("=== TEST 1: Plain text input ===")
sample_text = """
I am a software engineer with 2 years of experience.
Skills: Python, TensorFlow, SQL, Docker, REST APIs, Git.
Built ML models using scikit-learn and deployed on AWS.
Worked with React for frontend and FastAPI for backend.
"""
skills = extract_skills(sample_text)
print("Extracted:", skills)

print("\n=== TEST 2: TXT file simulation ===")
file_bytes = sample_text.encode("utf-8")
text = extract_text(file_bytes, "resume.txt")
skills2 = extract_skills(text)
print("From .txt file:", skills2)
