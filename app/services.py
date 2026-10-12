import json
import os
from openai import OpenAI

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are a technical recruiter. Compare the resume with the job description.
Respond with a JSON object containing exactly these keys:
- "match_score": integer from 0 to 100 for how well the resume fits the job
- "missing_skills": list of short strings, skills the job needs that the resume lacks
- "suggestions": list of short, actionable strings to improve the resume for this job"""

_client = None


def get_client():
    # Created on first use so the app can start (and be tested) without an OpenAI key
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


def parse_analysis(raw):
    """Validate the model's JSON and normalise it into a fixed shape."""
    try:
        data = json.loads(raw)
        score = int(round(float(data["match_score"])))
    except (ValueError, TypeError, KeyError) as e:
        raise ValueError(f"Invalid analysis from LLM: {e}") from e

    return {
        "match_score": max(0, min(100, score)),
        "missing_skills": [str(s) for s in data.get("missing_skills", [])],
        "suggestions": [str(s) for s in data.get("suggestions", [])],
    }


def analyze_resume(resume_text, job_description):
    response = get_client().chat.completions.create(
        model=MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}"},
        ],
    )

    return parse_analysis(response.choices[0].message.content)
