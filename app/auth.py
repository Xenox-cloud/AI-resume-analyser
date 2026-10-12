from fastapi import Header, HTTPException, status
import os
import secrets


def verify_api_key(x_api_key: str = Header(...)):
    expected = os.getenv("API_KEY")
    # Refuse every request if the server has no key configured, and compare in constant time
    if not expected or not secrets.compare_digest(x_api_key, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
