from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address


def get_api_key(request: Request):
    # Rate-limit per API key; fall back to client IP when the header is missing
    return request.headers.get("x-api-key") or get_remote_address(request)


limiter = Limiter(key_func=get_api_key)
