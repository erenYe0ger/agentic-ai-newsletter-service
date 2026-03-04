from sqlalchemy import Table, Column, Integer, String, Text, DateTime, Float, MetaData
from session import engine
import datetime


def init_db():

    metadata = MetaData()

    today = datetime.datetime.now(datetime.UTC).strftime("%d_%m_%Y")
    table_name = f"articles_{today}"

    Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True),
        Column("title", String, nullable=False),
        Column("link", String, unique=True, nullable=False),
        Column("summary", Text, nullable=False),
        Column("similarity_score", Float),
        Column("published_at", DateTime)
    )

    metadata.create_all(bind=engine)

    print(f"Created/verified table: {table_name}")


if __name__ == "__main__":
    init_db()