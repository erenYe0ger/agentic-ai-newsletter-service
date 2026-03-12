# 🤖 Agentic AI Newsletter Service

An autonomous AI-powered system that discovers, summarizes, ranks, and delivers the most relevant AI and technology news directly to subscribers via email. 

This project demonstrates a production-style AI pipeline combining modern backend architecture with agentic workflows.

---

## 🚀 Features & Pipeline

The system transforms raw web content into a concise, structured daily digest:

* 🛰️ **RSS Ingestion**: Monitors trusted AI and tech feeds.
* 📄 **Content Extraction**: Pulls full article text from source webpages.
* 🧠 **LLM Summarization**: Generates concise insights using transformer models.
* 📊 **Semantic Ranking**: Sorts articles by relevance to user interests.
* 🗄️ **Persistent Storage**: Manages subscriber data and articles in PostgreSQL.
* 📧 **Automated Delivery**: Sends high-quality HTML newsletters via Gmail API daily at 8:00 IST.
* 🐳 **Cloud Native**: Fully containerized with Docker and deployed to the cloud.

---

## 🌐 Live Deployment

| Component | URL |
| :--- | :--- |
| **Frontend (Subscription)** | [https://daily-tech-digest.netlify.app](https://daily-tech-digest.netlify.app) |
| **Backend API** | [https://agentic-ai-newsletter-service.onrender.com](https://agentic-ai-newsletter-service.onrender.com) |

> `[!IMPORTANT]`
> This `deploy` branch contains the cloud-ready configuration. If you wish to run the pipeline locally with a local PostgreSQL container, please switch to the `main` branch.

---

## 🏗️ System Architecture

* **Frontend**: Static landing page hosted on **Netlify**.
* **Backend**: **FastAPI** server running inside a **Docker** container on **Render**.
* **Database**: **PostgreSQL** managed instance on **Render**.
* **Email**: **Gmail API** utilizing secure **OAuth2** authentication.

---

## ⚙️ Pipeline Flow

1.  **Subscription**: User enters email on the frontend → sent to `/subscribe`.
2.  **Persistence**: Backend stores the email in PostgreSQL.
3.  **Onboarding**: An automated Welcome Email is dispatched.
4.  **AI Orchestration**: The pipeline triggers:
    * Fetch RSS → Extract → Summarize → Rank → Build Mail → Dispatch.

---

## 🛠️ Deployment Guide

Follow these steps to reproduce the deployment environment.

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/erenYe0ger/agentic-ai-newsletter-service.git
cd agentic-ai-newsletter-service
git checkout deploy
```

### 2️⃣ Setup Gmail API (OAuth)
The system uses the Gmail API for secure delivery.

1.  **Google Cloud Project**: Create a new project at [Google Cloud Console](https://console.cloud.google.com).
2.  **Enable API**: Search for and enable the **Gmail API**.
3.  **Credentials**: Create an **OAuth Client ID** (Type: Desktop Application). Download the JSON and rename it to `credentials.json` in your root folder.
4.  **Generate Token**: Create `generate_token.py`:
    ```python
    import pickle
    from google_auth_oauthlib.flow import InstalledAppFlow
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    with open('token.pickle','wb') as token:
        pickle.dump(creds, token)
    print("Token generated successfully")
    ```
5.  **Encode Token**: Run the script, then encode the resulting `token.pickle`:
    ```bash
    python -c "import base64;print(base64.b64encode(open('token.pickle','rb').read()).decode())"
    ```
    *Copy the output string for the `GMAIL_TOKEN` environment variable. Delete the files just created.*

### 3️⃣ Create PostgreSQL Database (Render)
1.  Create a new **PostgreSQL** instance on [Render](https://render.com).
2.  Set Database: `newsletter_db`, User: `newsletter_user`.
3.  Copy the **Internal Database URL** (e.g., `postgres://user:pass@host:port/db`).

### 4️⃣ Deploy Backend on Render
1.  Create a **New Web Service** and connect this repository.
2.  **Branch**: `deploy`.
3.  **Region**: Same as your database.
4.  **Runtime**: Docker.
5.  **Environment Variables**:
    * `EMAIL_ADDRESS`: Your Gmail address.
    * `GMAIL_TOKEN`: The base64 string from Step 2.
    * `DATABASE_URL`: The Internal URL from Step 3.
    * `HF_API_TOKEN`: Your HuggingFace API token.
    * `HF_TOKEN`: Your HuggingFace API token.

### 5️⃣ Deploy Frontend (Netlify)
1.  Create **New Site from Git** on Netlify.
2.  **Base Directory**: `frontend`.
3.  **Publish Directory**: `frontend`.
4.  **Build Command**: *Leave blank*.

---

## 🛠️ Manual Controls
To manually trigger the full curation and delivery pipeline:
```bash
curl -X POST https://agentic-ai-newsletter-service.onrender.com/run-pipeline
```

---

## ✍️ Author
**Goutam Mukherjee**