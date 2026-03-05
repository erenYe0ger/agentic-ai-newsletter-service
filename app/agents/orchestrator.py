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


class Orchestrator:
    """
    Main orchestration agent for the newsletter pipeline.

    Pipeline flow:
        RSS → Extract → Summarize → Rank → Store → Email

    This class coordinates all agents and services while keeping
    database operations separated in the repository layer.
    """

    def __init__(self):

        # Database session
        self.db = SessionLocal()

        # Repository layer handles database operations
        self.repo = ArticleRepository(self.db)

        # Pipeline components
        self.rss_service = RSSService()
        self.extractor = ExtractorService()
        self.summarizer_agent = SummarizationAgent()
        self.ranking_agent = RankingAgent()
        self.email_agent = EmailAgent()


    def run(self):

        print("[Pipeline] Loading RSS feeds...")

        # Load RSS sources from config
        with open("app/config/rss_sources.json") as f:
            feeds = json.load(f)["feeds"]

        # Current UTC time for filtering
        now = datetime.now(timezone.utc)

        # Determine today's database table
        table_name = self.repo.get_today_table()

        for url in feeds:

            # Fetch articles from RSS feed
            items = self.rss_service.fetch(url)

            for item in items:

                published_raw = item.get("published")

                # Skip entries without publish date
                if not published_raw:
                    continue

                try:
                    published = parsedate_to_datetime(published_raw)
                except Exception:
                    continue

                # Skip articles older than 24 hours
                if now - published > timedelta(hours=24):
                    continue

                print(f"[Pipeline] Processing: {item['title']}")

                # Extract full article content
                raw_text = self.extractor.extract(item["link"])

                description = item.get("description", "")

                # Combine signals for summarization
                combined_text = f"""
TITLE:
{item['title']}

DESCRIPTION:
{description}

CONTENT:
{raw_text}
"""

                # Generate article summary
                summary = self.summarizer_agent.run(combined_text)

                article = {
                    "title": item["title"],
                    "link": item["link"],
                    "summary": summary,
                }

                # Compute semantic relevance score
                score = self.ranking_agent.score(article)

                # Store article in database
                self.repo.upsert_article(
                    table_name=table_name,
                    article=article,
                    score=score,
                    published_raw=published_raw,
                )

        print("[Pipeline] Fetching top ranked articles...")

        # Retrieve best articles for newsletter
        top_articles = self.repo.fetch_top_articles(table_name)

        deepmind_article = None
        hf_article = None
        others = []

        for article in top_articles:

            link = article["link"]

            if not deepmind_article and "deepmind.google" in link:
                deepmind_article = article

            elif not hf_article and "huggingface.co" in link:
                hf_article = article

            else:
                others.append(article)


        final_articles = []

        # 1️⃣ Always DeepMind first if available
        if deepmind_article:
            final_articles.append(deepmind_article)

        # 2️⃣ Always HuggingFace second if available
        if hf_article:
            final_articles.append(hf_article)

        # 3️⃣ Fill remaining slots with top ranked articles
        for article in others:
            if len(final_articles) >= 5:
                break
            final_articles.append(article)


        self.email_agent.send(final_articles)

        print("[Pipeline] Completed.")