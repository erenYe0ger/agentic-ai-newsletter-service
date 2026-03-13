from app.db.session import SessionLocal

from app.agents.summarization_agent import SummarizationAgent
from app.agents.ranking_agent import RankingAgent
from app.agents.email_agent import EmailAgent

from app.services.rss_service import RSSService
from app.services.extractor_service import ExtractorService
from app.services.article_repository import ArticleRepository

from email.utils import parsedate_to_datetime
from datetime import datetime, timezone, timedelta

import json
from typing import Any

from app.utils.article_selector import select_final_articles


class Orchestrator:
    """
    Main orchestration agent for the newsletter pipeline.

    Pipeline flow:
        RSS → Extract → Summarize → Rank → Store

    Email delivery is triggered separately.
    """

    def __init__(self) -> None:

        # Database session
        self.db = SessionLocal()

        # Repository layer handles database operations
        self.repo: ArticleRepository = ArticleRepository(self.db)

        # Pipeline components
        self.rss_service: RSSService = RSSService()
        self.extractor: ExtractorService = ExtractorService()
        self.summarizer_agent: SummarizationAgent = SummarizationAgent()
        self.ranking_agent: RankingAgent = RankingAgent()
        self.email_agent: EmailAgent = EmailAgent()


    def collect_news(self) -> None:

        print("[CollectNews] Loading RSS feeds...")

        # Load RSS sources from config
        with open("app/config/rss_sources.json") as f:
            feeds: list[str] = json.load(f)["feeds"]

        # Current UTC time for filtering
        now: datetime = datetime.now(timezone.utc)

        # Determine today's database table
        table_name: str = self.repo.get_today_table()

        for url in feeds:

            items: list[dict[str, Any]] = self.rss_service.fetch(url)

            for item in items:

                published_raw: str | None = item.get("published")

                if not published_raw:
                    continue

                try:
                    published: datetime = parsedate_to_datetime(published_raw)
                except Exception:
                    continue

                if now - published > timedelta(hours=24):
                    continue

                print(f"[CollectNews] Processing: {item['title']}")

                raw_text: str = self.extractor.extract(item["link"])

                description: str = item.get("description", "")

                combined_text: str = f"""
TITLE:
{item['title']}

DESCRIPTION:
{description}

CONTENT:
{raw_text}
"""

                summary: str = self.summarizer_agent.run(combined_text)

                article: dict[str, str] = {
                    "title": item["title"],
                    "link": item["link"],
                    "summary": summary,
                }

                score: float = self.ranking_agent.score(article)

                self.repo.upsert_article(
                    table_name=table_name,
                    article=article,
                    score=score,
                    published_raw=published_raw,
                )

        print("[CollectNews] Completed.")


    def send_digest(self) -> None:

        print("[SendDigest] Preparing newsletter...")

        table_name = self.repo.get_today_table()

        top_articles = self.repo.fetch_top_articles(table_name)

        final_articles = select_final_articles(top_articles)

        if not final_articles:
            print("[SendDigest] No articles available.")
            return

        self.email_agent.send(final_articles)

        print("[SendDigest] Emails sent successfully.")