# AI Resume Analyzer API

A production-ready backend service that analyzes resumes against job descriptions using LLMs. The system evaluates candidate-job fit, identifies missing skills, and provides actionable suggestions to improve alignment.

This project demonstrates real-world backend engineering practices including API design, authentication, rate limiting, logging, and AI integration.

---

## 🚀 Features

* Resume parsing from PDF files
* AI-powered evaluation using LLMs
* Match score estimation and skill gap analysis
* RESTful API built with FastAPI
* API key-based authentication
* Rate limiting to prevent abuse
* Request logging and usage tracking
* PostgreSQL integration for persistence
* Dockerized for consistent deployment

---

## 🧱 Tech Stack

* Backend: FastAPI
* Database: PostgreSQL
* AI: OpenAI API (LLM-based analysis)
* Containerization: Docker
* Rate Limiting: SlowAPI
* File Processing: PyPDF2

---

## 📦 Project Structure

```
resume-analyzer/
│
├── app/
│   ├── main.py          # FastAPI entry point
│   ├── routes.py        # API endpoints
│   ├── services.py      # LLM integration logic
│   ├── models.py        # Database models
│   ├── database.py      # DB connection setup
│   ├── auth.py          # API key authentication
│   ├── utils.py         # PDF parsing utilities
│   └── logger.py        # Logging configuration
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env (not committed)
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/Xenox-cloud/AI-resume-analyser.git
cd AI-resume-analyser
```

---

### 2. Create environment variables

Copy `.env.example` to `.env` and fill in your own values:

```
OPENAI_API_KEY=your_openai_api_key
API_KEY=your_secure_api_key
POSTGRES_PASSWORD=change-me
DATABASE_URL=postgresql://postgres:change-me@localhost:5432/resume_db
```

---

### 3. Run locally (without Docker)

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

### 4. Run with Docker

```
docker compose up --build
```

---

## 🌐 API Documentation

Once running:

```
http://localhost:8000/docs
```

---

## 🔐 Authentication

All endpoints are protected using API key authentication.

Include the following header in every request:

```
x-api-key: your_secure_api_key
```

---

## 📡 API Endpoints

### POST /analyze

Analyze a resume against a job description.

**Request:**

* Content-Type: multipart/form-data
* Fields:

  * file: PDF resume
  * job_description: text

**Response:**

```
{
  "id": 12,
  "match_score": 78,
  "missing_skills": ["Docker", "CI/CD"],
  "suggestions": ["Quantify the impact of your FastAPI projects"]
}
```

The model is called in JSON mode and its output is validated (score clamped to 0–100) before the score is stored. Non-PDF uploads return `415`; an invalid model response returns `502`.

---

### GET /usage

Returns total number of API requests processed.

```
{
  "total_requests": 12
}
```

---

## 🚦 Rate Limiting

* Limit: 5 requests per minute per API key
* Prevents abuse and controls API cost

---

## 📊 Logging & Monitoring

* Logs each API request
* Tracks usage in PostgreSQL
* Enables basic analytics and cost monitoring

---

## 🧠 System Design Highlights

* Stateless API design with token-based access
* Separation of concerns (routes, services, DB, utils)
* Scalable architecture with containerization
* LLM integration for real-world AI use case
* Defensive engineering with rate limiting and authentication

---

## ⚠️ Security Notes

* API keys are stored in environment variables
* `.env` is excluded from version control
* Sensitive credentials are never hardcoded
* API keys are compared in constant time, and every request is refused if no key is configured

---

## 🧪 Tests

The tests fake the LLM call and use SQLite, so they need no OpenAI key or PostgreSQL:

```
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

They cover structured analysis and score storage, API-key checks, PDF validation, the 5/minute rate limit, and parsing of the model's JSON.

---

## 📌 Future Improvements

* User-based authentication with JWT
* Frontend dashboard for analytics
* Async processing for large files
* Caching for repeated queries

---

## 👨‍💻 Author

Musfiq Alam
Aspiring Backend & AI Engineer

---

## 📄 License

This project is for educational and demonstration purposes.
