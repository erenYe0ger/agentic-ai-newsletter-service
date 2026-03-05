# 🤖 Agentic AI Newsletter Service

**Agentic AI Newsletter Service** is an automated pipeline that collects the latest tech and AI news, summarizes articles using large language models, ranks them by relevance, and delivers a curated daily newsletter via email. 📬

> The system runs fully autonomously and transforms raw web content into a concise, structured daily digest. 🚀

---

## 🌟 Overview

This project implements an **agent-driven information pipeline** that automatically curates relevant tech and AI news.

The pipeline performs the following steps:

1. 🛰 **Fetch** articles from RSS feeds
2. 📄 **Extract** full article content from webpages
3. 🧠 **Generate** concise summaries using LLMs
4. 📊 **Rank** articles based on semantic similarity to AI topics
5. 🗄 **Store** processed articles in PostgreSQL
6. 📧 **Deliver** the top articles as a styled HTML newsletter

The result is a fully automated **AI-powered information curation system**. 🛠️

---

## 🛠 Tech Stack

### ⚙️ Backend
- **Language:** Python 🐍

### 🧠 AI / NLP
- **Inference:** HuggingFace Inference API 🤗
- **Embeddings:** SentenceTransformers

### 🕸 Data Processing
- **Parsing:** BeautifulSoup 🥣
- **Feeds:** Feedparser

### 🗄 Database
- **Engine:** PostgreSQL 🐘
- **ORM:** SQLAlchemy

### 🏗 Infrastructure
- **Containerization:** Docker 🐳
- **Environment:** UV (Python environment manager) ⚡

### 📧 Email Delivery
- **Protocol:** SMTP

---

## 🚀 Running the Project

### 1️⃣ Clone the repository
```bash
git clone https://github.com/erenYe0ger/agentic-ai-newsletter-service.git
cd agentic-ai-newsletter-service
```

### 2️⃣ Prerequisites & Configuration
* **Docker Desktop:** Ensure **Docker Desktop** is installed and running on your machine to host the PostgreSQL database.
* **Email App Password:** For using Gmail, you must generate an **App Password** (not your regular password). You can do this at [Google App Passwords](https://myaccount.google.com/apppasswords).

### 3️⃣ Setup config files
Inside ```config/``` directory, add a ```recipients.json``` file to manage your mailing list:
```json
{
  "recipients": [
    "example@gmail.com",
    "example2@gmail.com",
    "example3@gmail.com",
  ]
}
```

### 4️⃣ Create a .env file
```text
DATABASE_URL=postgresql://user:password@localhost:5432/tech_news
HF_API_TOKEN=your_huggingface_token
HF_TOKEN=your_huggingface_token
EMAIL_ADDRESS=your_email
EMAIL_APP_PASSWORD=your_email_app_password
```

### 5️⃣ Run the pipeline
```bash
uv run main.py
```

The pipeline will automatically:
- ✅ Start PostgreSQL via Docker
- ✅ Initialize database tables
- ✅ Fetch articles from RSS feeds
- ✅ Extract article content
- ✅ Generate AI summaries
- ✅ Rank articles by relevance
- ✅ Send the newsletter email

---

## 📤 Output

Each newsletter email contains:
- 📌 **Curated article titles**
- 📝 **AI-generated summaries**
- 🔗 **Links to the original articles**
- 🔥 **The most relevant AI and tech news of the day**

*All emails are delivered using a clean HTML newsletter layout.* ✨

---

**Author:** [Goutam Mukherjee](https://github.com/erenYe0ger) ✍️