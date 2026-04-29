from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"

    id = Column(Integer, primary_key=True, index=True)
    resume_text = Column(Text)
    job_description = Column(Text)
    score = Column(Integer)
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    api_key = Column(String)