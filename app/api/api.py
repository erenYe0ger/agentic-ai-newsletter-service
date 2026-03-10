from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import text
from app.db.session import engine


app = FastAPI()


class SubscribeRequest(BaseModel):
    email: str


@app.post("/subscribe")
def subscribe(data: SubscribeRequest):
    """
    Add a new subscriber to the database.
    """

    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO subscribers (email) VALUES (:email)"),
            {"email": data.email},
        )
        conn.commit()

    return {"status": "subscribed"}