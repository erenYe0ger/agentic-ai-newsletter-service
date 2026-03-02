# Agentic AI Newsletter Service

A fully automated, agentic pipeline that collects technology news, extracts article content, summarizes it using a HuggingFace LLM, and stores it in a PostgreSQL database running inside Docker. This project is built using modern Python practices (UV, pyproject.toml, modular architecture) and is designed to evolve into a personalized daily AI-driven newsletter.

---

## 🚀 Current Features (Completed Milestone)

### ✔ RSS Scraping  
Fetches fresh technology news articles from TechCrunch via RSS.

### ✔ HTML Content Extraction  
Scrapes article pages and extracts clean text (no ads, no related posts, no junk).

### ✔ LLM Summarization  
Summarizes extracted content using a free-tier HuggingFace model (`Qwen/Qwen2.5-72B-Instruct`).

### ✔ PostgreSQL + Docker  
Fully working database setup:
- Docker-managed PostgreSQL instance  
- SQLAlchemy ORM models  
- Automatic table creation  
- Inserted articles saved successfully  

### ✔ End-to-End Automated Pipeline  
A single command runs:
1. Start Docker Postgres  
2. Initialize DB  
3. Scrape articles  
4. Extract content  
5. Summarize  
6. Insert to DB  

---

## 🛠 Tech Stack

- **Python 3.13+**
- **UV** (pyproject-based dependency + env management)
- **SQLAlchemy** (ORM)
- **PostgreSQL** (Docker)
- **HuggingFace Inference API**
- **Requests / Feedparser / BeautifulSoup**
- **Modular Service Architecture**
- **VS Code**

---

## 🎯 Next Steps (Upcoming Phases)

- Multi-source scraping (The Verge, Ars Technica, Wired)
- Email formatter & daily digest emails
- User profile → personalized ranking system
- Render deployment + cron scheduler
- Robust logging + monitoring
- Alembic migrations


---

This is the foundational milestone: **the entire ingestion & summarization pipeline is fully operational.**