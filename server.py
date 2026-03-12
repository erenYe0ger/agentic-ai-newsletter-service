import os
import uvicorn
import threading
import time
import schedule

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from sqlalchemy import text

from app.db.session import engine
from app.db.init_db import init_db
from app.agents.orchestrator import Orchestrator

from fastapi.middleware.cors import CORSMiddleware


# FastAPI application
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request body for subscribe endpoint
class SubscribeRequest(BaseModel):
    email: EmailStr


from app.services.email_service import EmailService

mailer = EmailService()



from app.utils.sub_layout import wrap_email

def send_subscribe_email(email: str):

    content = """
<h2 style="font-family:'Playfair Display',serif; font-size:30px; color:#1E293B; margin: 0 0 15px 0; line-height: 1.2;">
Welcome to the Pipeline!
</h2>
<p style="font-size:18px; color:#475569; margin: 0 0 10px 0; font-weight: 400;">
You're officially subscribed to the <strong>Agentic AI Digest</strong>.
</p>
<p style="font-size:16px; color:#64748B; margin: 10px 0 0 0; line-height: 1.6;">
Our autonomous agents are currently scanning the horizon for the latest AI breakthroughs, research papers, and tool launches. We filter the noise so you only get the signal.
</p>
<p style="font-size:16px; color:#6366F1; margin: 25px 0 0 0; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
Your first digest arrives shortly.
</p>
<p style="font-size:16px; color:#ec0808; margin: 25px 0 0 0; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
You'll receive a beautifully curated newsletter every day at 08:00 IST, packed with the most important AI news and insights in last 24 hours.
</p>
"""

    html = wrap_email(content)

    mailer.send_email(
        to_email=email,
        subject="Welcome to the Pipeline!",
        html_content=html
    )




def send_unsubscribe_email(email: str):

    content = """
<h2 style="font-family:'Playfair Display',serif; font-size:30px; color:#1E293B; margin: 0 0 15px 0; line-height: 1.2;">
You have been unsubscribed!
</h2>
<p style="font-size:16px; color:#64748B; margin: 10px 0 0 0; line-height: 1.6;">
You will no longer receive the Daily Digest. We're sorry to see you go!
</p>
<p style="font-size:16px; color:#6366F1; margin: 25px 0 0 0; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
If you change your mind, you can always subscribe again to stay updated with the latest in AI and Tech.
</p>
"""

    html = wrap_email(content)

    mailer.send_email(
        to_email=email,
        subject="You have been unsubscribed",
        html_content=html
    )



# Add a subscriber to the database
import threading

@app.post("/subscribe")
def subscribe(data: SubscribeRequest):

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                INSERT INTO subscribers (email)
                VALUES (:email)
                ON CONFLICT (email) DO NOTHING
                RETURNING email
            """),
            {"email": data.email},
        )
        inserted = result.fetchone()
        conn.commit()

    # email already existed
    if inserted is None:
        return {"status": "already_subscribed"}

    # send welcome email
    send_subscribe_email(data.email)

    # run pipeline in background
    def run_pipeline():
        init_db()
        Orchestrator().run()

    import threading
    threading.Thread(target=run_pipeline, daemon=True).start()

    return {"status": "subscribed"}



from fastapi.responses import HTMLResponse, RedirectResponse

@app.get("/unsubscribe")
def unsubscribe(email: str):

    with engine.connect() as conn:
        result = conn.execute(
            text("DELETE FROM subscribers WHERE email=:email RETURNING email"),
            {"email": email}
        )
        deleted = result.fetchone()
        conn.commit()

    # send goodbye email
    if deleted:
        send_unsubscribe_email(email)

    return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
<title>Unsubscribed</title>
<style>
body {
background: #0a0a0c;
color: white;
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
display: flex;
justify-content: center;
align-items: center;
height: 100vh;
margin: 0;
}

.box {
text-align: center;
padding: 40px 60px;
border-radius: 16px;
background: rgba(255,255,255,0.05);
backdrop-filter: blur(20px);
border: 1px solid rgba(255,255,255,0.1);
}

h1 {
margin: 0 0 10px 0;
font-size: 28px;
}

p {
margin: 0;
color: #9ca3af;
font-size: 14px;
}
</style>
<link rel="icon" type="image/svg+xml" href="https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png">
</head>
<body>
<div class="box">
<h1>You have been unsubscribed</h1>
<p>You may close this tab.</p>
</div>
</body>
</html>
""")



@app.get("/")
def root():
    return {
        "service": "Agentic AI Newsletter Service",
        "status": "running",
        "message": "Autonomous AI news pipeline is active."
    }


# Manually trigger the newsletter pipeline
@app.post("/run-pipeline")
def run_pipeline():

    init_db()  # ensure tables exist
    Orchestrator().run()

    return {"status": "pipeline executed"}


# Background scheduler (runs every day at 02:30 UTC = 08:00 IST)
def scheduler_loop():

    def daily_job():
        init_db()
        Orchestrator().run()

    schedule.every().day.at("02:30").do(daily_job)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":

    # Ensure tables exist on server start
    init_db()

    # Run scheduler in background
    threading.Thread(target=scheduler_loop, daemon=True).start()

    # Start FastAPI server
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )