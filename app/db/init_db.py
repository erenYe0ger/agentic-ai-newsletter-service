from sqlalchemy import Table, Column, Integer, String, Text, DateTime, Float, MetaData
from session import engine
import datetime


def create_daily_articles_table() -> str:
    """
    Creates a new articles table for the current day.

    Table naming convention:
        articles_DD_MM_YYYY

    Example:
        articles_05_03_2026

    The table stores scraped articles along with their
    summary and semantic ranking score.
    """

    metadata: MetaData = MetaData()

    # Generate today's table name
    today: str = datetime.datetime.now(datetime.UTC).strftime("%d_%m_%Y")
    table_name: str = f"articles_{today}"

    # Define table schema
    Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True),
        Column("title", String, nullable=False),
        Column("link", String, unique=True, nullable=False),
        Column("summary", Text, nullable=False),
        Column("similarity_score", Float),
        Column("published_at", DateTime),
    )

    # Create table if it does not exist
    metadata.create_all(bind=engine)

    return table_name


def init_db() -> None:
    """
    Initialize database by ensuring today's article table exists.
    """
    table: str = create_daily_articles_table()
    print(f"Created/verified table: {table}")


if __name__ == "__main__":
    init_db()