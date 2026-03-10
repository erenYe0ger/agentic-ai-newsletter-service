import os
import uvicorn
import threading
import time
import schedule

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import text

from app.db.session import engine
from app.agents.orchestrator import Orchestrator


from app.db.init_db import init_db


# FastAPI server
app = FastAPI()


# Request body model for /subscribe
class SubscribeRequest(BaseModel):
    email: str


# Add a new subscriber
@app.post("/subscribe")
def subscribe(data: SubscribeRequest):

    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO subscribers (email) VALUES (:email)"),
            {"email": data.email},
        )
        conn.commit()

    return {"status": "subscribed"}


# Manually trigger the newsletter pipeline
@app.post("/run-pipeline")
def run_pipeline():

    init_db()  # ensure today's table exists

    Orchestrator().run()
    return {"status": "pipeline executed"}


# Daily scheduler (02:30 UTC = 08:00 IST)
def scheduler_loop():

    schedule.every().day.at("02:30").do(lambda: [init_db(), Orchestrator().run()])

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":

    # run scheduler in background
    threading.Thread(target=scheduler_loop, daemon=True).start()

    # start FastAPI server
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )