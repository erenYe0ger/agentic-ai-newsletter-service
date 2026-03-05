from sqlalchemy import text
from sqlalchemy.orm import Session
from email.utils import parsedate_to_datetime
import datetime
from typing import Any


class ArticleRepository:
    """
    Handles all database operations related to articles.

    Keeps database logic separate from the pipeline logic.
    Responsible for inserting, updating, and retrieving
    ranked articles.
    """

    def __init__(self, db: Session) -> None:
        self.db: Session = db

    def get_today_table(self) -> str:
        """
        Returns today's dynamic table name.
        Example: articles_05_03_2026
        """
        today: str = datetime.datetime.now(datetime.UTC).strftime("%d_%m_%Y")
        return f"articles_{today}"

    def upsert_article(
        self,
        table_name: str,
        article: dict[str, str],
        score: float,
        published_raw: str,
    ) -> None:
        """
        Insert article if it does not exist.
        Otherwise update the existing record.
        """

        try:
            published: datetime.datetime | None = parsedate_to_datetime(published_raw)
        except Exception:
            published = None

        exists: Any = self.db.execute(
            text(f"SELECT id FROM {table_name} WHERE link=:link"),
            {"link": article["link"]},
        ).fetchone()

        if exists:

            self.db.execute(
                text(
                    f"""
                    UPDATE {table_name}
                    SET
                        title=:title,
                        summary=:summary,
                        similarity_score=:score,
                        published_at=:published
                    WHERE link=:link
                    """
                ),
                {
                    "title": article["title"],
                    "summary": article["summary"],
                    "score": score,
                    "published": published,
                    "link": article["link"],
                },
            )

        else:

            self.db.execute(
                text(
                    f"""
                    INSERT INTO {table_name}
                    (title, link, summary, similarity_score, published_at)
                    VALUES (:title, :link, :summary, :score, :published)
                    """
                ),
                {
                    "title": article["title"],
                    "link": article["link"],
                    "summary": article["summary"],
                    "score": score,
                    "published": published,
                },
            )

        self.db.commit()

    def fetch_top_articles(self, table_name: str, limit: int = 15) -> list[dict[str, str]]:
        """
        Fetch top ranked articles for newsletter generation.

        Default limit increased to 20 so the orchestrator
        can perform source balancing (DeepMind + HuggingFace
        preference) before selecting the final 5 articles.
        """

        rows: Any = self.db.execute(
            text(
                f"""
                SELECT title, link, summary
                FROM {table_name}
                WHERE summary != 'Summary unavailable.'
                ORDER BY similarity_score DESC
                LIMIT :limit
                """
            ),
            {"limit": limit},
        ).fetchall()

        return [
            {"title": r[0], "link": r[1], "summary": r[2]}
            for r in rows
        ]