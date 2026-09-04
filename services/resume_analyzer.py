import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_resume(resume_text):

    prompt = f"""
You are an expert technical interviewer.

Analyze the following candidate resume.

RESUME:
{resume_text}

Extract:

1. Technical skills
2. Programming languages
3. Technologies/tools
4. Projects
5. Work experience

Then generate 5 personalized technical interview questions
based specifically on this resume.

Questions should test whether the candidate actually
understands the technologies and projects mentioned.

Return ONLY valid JSON in this format:

{{
    "skills": [],
    "languages": [],
    "technologies": [],
    "projects": [],
    "experience": [],
    "questions": []
}}
if st.button("🎯 Start Resume-Based Interview", use_container_width=True):

    resume_questions = analysis["questions"]

    st.session_state["questions"] = resume_questions
    st.session_state["current_question"] = 0
    st.session_state["answers"] = []
    st.session_state["current_evaluation"] = None
    st.session_state["started"] = True
    st.session_state["interview_completed"] = False
    st.session_state["resume_based"] = True

    st.rerun()
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)