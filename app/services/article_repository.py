from sqlalchemy import text
from email.utils import parsedate_to_datetime
import datetime


class ArticleRepository:
    """
    Handles all database operations related to articles.
    Keeps database logic separate from pipeline logic.
    """

    def __init__(self, db):
        self.db = db

    def get_today_table(self) -> str:
        today = datetime.datetime.now(datetime.UTC).strftime("%d_%m_%Y")
        return f"articles_{today}"

    def upsert_article(self, table_name: str, article: dict, score: float, published_raw: str):

        try:
            published = parsedate_to_datetime(published_raw)
        except Exception:
            published = None

        exists = self.db.execute(
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

    def fetch_top_articles(self, table_name: str, limit: int = 5):

        rows = self.db.execute(
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