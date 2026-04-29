import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_resume(resume_text, job_description):
    prompt = f"""
    Compare the resume with the job description.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Return:
    - Match Score (0-100)
    - Missing Skills
    - Suggestions
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content