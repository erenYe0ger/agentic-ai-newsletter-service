import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

print("LOADED DB URL:", os.getenv("DATABASE_URL"))
DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)