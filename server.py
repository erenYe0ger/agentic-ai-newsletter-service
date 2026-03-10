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


app = FastAPI()


class SubscribeRequest(BaseModel):
    email: str


@app.post("/subscribe")
def subscribe(data: SubscribeRequest):

    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO subscribers (email) VALUES (:email)"),
            {"email": data.email},
        )
        conn.commit()

    return {"status": "subscribed"}


@app.post("/run-pipeline")
def run_pipeline():

    Orchestrator().run()
    return {"status": "pipeline executed"}


def scheduler_loop():

    schedule.every().day.at("02:30").do(lambda: Orchestrator().run())  # 08:00 IST

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":

    threading.Thread(target=scheduler_loop, daemon=True).start()

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )