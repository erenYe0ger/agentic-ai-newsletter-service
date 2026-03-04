from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database connection string
DATABASE_URL: str = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session factory used throughout the application
# Provides database sessions for queries and transactions
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)