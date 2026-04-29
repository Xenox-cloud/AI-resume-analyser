from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from .database import Base, engine
from .routes import router

def get_api_key(request: Request):
    return request.headers.get("x-api-key")

limiter = Limiter(key_func=get_api_key)

app = FastAPI()

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

Base.metadata.create_all(bind=engine)

app.include_router(router)