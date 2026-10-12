from dotenv import load_dotenv

# Load .env before any module reads environment variables
load_dotenv()

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from .database import Base, engine
from .limiter import limiter
from .routes import router

app = FastAPI(title="AI Resume Analyzer API")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

Base.metadata.create_all(bind=engine)

app.include_router(router)
