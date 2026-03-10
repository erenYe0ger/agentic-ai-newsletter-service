from sqlalchemy import Table, Column, Integer, String, Text, DateTime, Float, MetaData
from app.db.session import engine
import datetime


def create_daily_articles_table(metadata: MetaData) -> str:
    """
    Creates a new articles table for the current day.

    Table naming convention:
        articles_DD_MM_YYYY

    Example:
        articles_05_03_2026

    The table stores scraped articles along with their
    summary and semantic ranking score.
    """

    # Generate today's table name in UTC
    today: str = datetime.datetime.now(datetime.UTC).strftime("%d_%m_%Y")
    table_name: str = f"articles_{today}"

    # Define schema for the daily articles table
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

    return table_name


def create_subscribers_table(metadata: MetaData) -> None:
    """
    Creates the subscribers table used for storing
    newsletter subscribers.

    Schema:
        subscribers
        ├ id      (Primary Key)
        └ email   (Unique email address)
    """

    Table(
        "subscribers",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("email", String, unique=True, nullable=False),
    )


def init_db() -> None:
    """
    Initialize database by ensuring required tables exist.

    This function ensures:
        1. Daily articles table is created
        2. Subscribers table exists
    """

    metadata: MetaData = MetaData()

    # Create schema for daily article table
    table: str = create_daily_articles_table(metadata)

    # Create schema for subscribers table
    create_subscribers_table(metadata)

    # Apply schema to database (creates tables if not present)
    metadata.create_all(bind=engine)

    # Logging for visibility
    print(f"Created/verified table: {table}")
    print("Created/verified table: subscribers")


if __name__ == "__main__":
    init_db()