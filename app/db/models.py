from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    link = Column(String, unique=True, nullable=False)
    published_at = Column(DateTime, default=datetime.datetime.utcnow)
    full_text = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)