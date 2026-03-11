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
<h2 style="font-family:'Playfair Display',serif;font-size:28px;color:#1E293B;margin-bottom:20px;">
Subscription Confirmed!
</h2>

<p style="font-size:18px;color:#475569;margin:0;">
Welcome to the Agentic AI Digest.
</p>

<p style="font-size:16px;color:#64748B;margin-top:15px;">
Our agents summarize the most important AI breakthroughs
and deliver them straight to your inbox.
</p>

<p style="font-size:16px;color:#64748B;margin-top:20px;">
Your first digest is on its way.
</p>
"""

    html = wrap_email(content)

    mailer.send_email(
        to_email=email,
        subject="Welcome to the Agentic AI Digest",
        html_content=html
    )




def send_unsubscribe_email(email: str):

    content = """
<h2 style="font-family:'Playfair Display',serif;font-size:28px;color:#1E293B;margin-bottom:20px;">
You have been unsubscribed
</h2>

<p style="font-size:18px;color:#475569;margin:0;">
You will no longer receive the Agentic AI Digest.
</p>

<p style="font-size:16px;color:#64748B;margin-top:20px;">
We're sorry to see you go.
</p>
"""

    html = wrap_email(content)

    mailer.send_email(
        to_email=email,
        subject="You have been unsubscribed",
        html_content=html
    )



# Add a subscriber to the database
@app.post("/subscribe")
def subscribe(data: SubscribeRequest):

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO subscribers (email)
                VALUES (:email)
                ON CONFLICT (email) DO NOTHING
            """),
            {"email": data.email},
        )
        conn.commit()

    send_subscribe_email(data.email)
    
    # send today's digest immediately
    init_db()
    Orchestrator().run()

    return {"status": "subscribed"}


from fastapi import Query

@app.get("/unsubscribe")
def unsubscribe(email: str = Query(...)):

    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM subscribers WHERE email = :email"),
            {"email": email},
        )
        conn.commit()

    send_unsubscribe_email(email)

    return {"status": "unsubscribed"}


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