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
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer
```

---

### 2. Create environment variables

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key
API_KEY=your_secure_api_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/resume_db
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
docker-compose up --build
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
  "analysis": "Match Score: 78\nMissing Skills: ...\nSuggestions: ..."
}
```

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

---

## 📌 Future Improvements

* Structured score extraction from LLM output
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
