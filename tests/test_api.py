"""API tests that need no OpenAI key or PostgreSQL: the LLM call is faked and SQLite is used.

Run: pip install -r requirements.txt -r requirements-dev.txt && pytest
"""
import os

import pytest

os.environ["API_KEY"] = "test-key"
os.environ["DATABASE_URL"] = "sqlite:///./test_resume.db"

from fastapi.testclient import TestClient  # noqa: E402

from app import routes  # noqa: E402
from app.database import engine  # noqa: E402
from app.limiter import limiter  # noqa: E402
from app.main import app  # noqa: E402
from app.services import parse_analysis  # noqa: E402

HEADERS = {"x-api-key": "test-key"}
FAKE_RESULT = {"match_score": 72, "missing_skills": ["Docker"], "suggestions": ["Add metrics"]}


@pytest.fixture(autouse=True)
def fakes(monkeypatch):
    monkeypatch.setattr(routes, "extract_text_from_pdf", lambda f: "Python developer with FastAPI experience")
    monkeypatch.setattr(routes, "analyze_resume", lambda text, jd: dict(FAKE_RESULT))
    limiter.reset()
    yield


@pytest.fixture(scope="module")
def client():
    yield TestClient(app)
    engine.dispose()  # release the SQLite file so it can be deleted on Windows
    if os.path.exists("test_resume.db"):
        os.remove("test_resume.db")


def upload(client, headers=HEADERS, content_type="application/pdf"):
    return client.post(
        "/analyze",
        headers=headers,
        files={"file": ("cv.pdf", b"%PDF-1.4 fake", content_type)},
        data={"job_description": "Backend engineer, Python, Docker"},
    )


def test_analyze_returns_structured_result_and_stores_score(client):
    res = upload(client)
    assert res.status_code == 200
    body = res.json()
    assert body["match_score"] == 72
    assert body["missing_skills"] == ["Docker"]
    assert client.get("/usage", headers=HEADERS).json()["total_requests"] >= 1


def test_missing_or_wrong_api_key_rejected(client):
    assert upload(client, headers={"x-api-key": "wrong"}).status_code == 401
    assert client.get("/usage").status_code == 422  # header required
    assert client.get("/usage", headers={"x-api-key": "wrong"}).status_code == 401


def test_non_pdf_rejected(client):
    assert upload(client, content_type="text/plain").status_code == 415


def test_rate_limit_after_five_requests(client):
    codes = [upload(client).status_code for _ in range(6)]
    assert codes[:5] == [200] * 5
    assert codes[5] == 429


def test_parse_analysis_clamps_and_validates():
    assert parse_analysis('{"match_score": 140, "missing_skills": [], "suggestions": []}')["match_score"] == 100
    assert parse_analysis('{"match_score": "65.4"}')["match_score"] == 65
    with pytest.raises(ValueError):
        parse_analysis("not json")
    with pytest.raises(ValueError):
        parse_analysis('{"suggestions": []}')
