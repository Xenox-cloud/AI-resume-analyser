from fastapi import APIRouter, UploadFile, File, Form, Depends,Request
from sqlalchemy.orm import Session
from .database import SessionLocal
from .utils import extract_text_from_pdf
from .services import analyze_resume
from .models import ResumeAnalysis
from .auth import verify_api_key
from slowapi import Limiter
from slowapi.util import get_remote_address
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
    _: str = Depends(verify_api_key)
):
    api_key = request.headers.get("x-api-key")
    
    logger.info("Analyzing resume...")
    text = extract_text_from_pdf(file.file)

    result = analyze_resume(text, job_description)
    logger.info(f"API called with job description length: {len(job_description)}")

    record = ResumeAnalysis(
        resume_text=text,
        job_description=job_description,
        score=80, 
        feedback=result,
        pi_key=api_key
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    

    return {
        "analysis": result
    }
@router.get("/usage")
def get_usage(db: Session = Depends(get_db)):
    total_requests = db.query(ResumeAnalysis).count()

    return {
        "total_requests": total_requests
    }