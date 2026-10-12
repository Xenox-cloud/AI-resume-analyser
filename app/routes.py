import json
from fastapi import APIRouter, UploadFile, File, Form, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from .utils import extract_text_from_pdf
from .services import analyze_resume
from .models import ResumeAnalysis
from .auth import verify_api_key
from .limiter import limiter
from .logger import logger

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/analyze")
@limiter.limit("5/minute")
async def analyze(
    request: Request,
    file: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Resume must be a PDF")

    logger.info("Analyzing resume...")
    text = extract_text_from_pdf(file.file)
    if not text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in the PDF")

    try:
        result = analyze_resume(text, job_description)
    except ValueError as e:
        logger.error(str(e))
        raise HTTPException(status_code=502, detail="The AI model returned an invalid analysis")
    logger.info(f"API called with job description length: {len(job_description)}")

    record = ResumeAnalysis(
        resume_text=text,
        job_description=job_description,
        score=result["match_score"],
        feedback=json.dumps({"missing_skills": result["missing_skills"], "suggestions": result["suggestions"]}),
        api_key=request.headers.get("x-api-key")
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {"id": record.id, **result}

@router.get("/usage")
def get_usage(db: Session = Depends(get_db), _: None = Depends(verify_api_key)):
    total_requests = db.query(ResumeAnalysis).count()

    return {
        "total_requests": total_requests
    }
