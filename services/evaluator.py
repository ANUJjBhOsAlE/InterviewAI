import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def evaluate_answer(question, answer):

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer.

Question:
{question}

Candidate Answer:
{answer}

Give a score from 0 to 10 for:

- accuracy
- relevance
- completeness
- clarity

Then calculate an overall score.

Also provide short constructive feedback.

Return ONLY valid JSON.

Use exactly this format:

{{
    "accuracy": 0,
    "relevance": 0,
    "completeness": 0,
    "clarity": 0,
    "overall": 0,
    "feedback": "..."
}}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown code fences if Gemini returns them
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    result = json.loads(text)

    return result