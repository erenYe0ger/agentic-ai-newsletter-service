from app.db.session import SessionLocal

from app.agents.rss_scraper_agent import RSSScraperAgent
from app.agents.summarization_agent import SummarizationAgent
from app.agents.ranking_agent import RankingAgent
from app.agents.email_agent import EmailAgent

from app.services.extractor_service import ExtractorService
from app.services.article_repository import ArticleRepository


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

        # Repository for database operations
        self.repo = ArticleRepository(self.db)

        # Pipeline components
        self.rss_scraper = RSSScraperAgent()
        self.extractor = ExtractorService()
        self.summarizer_agent = SummarizationAgent()
        self.ranking_agent = RankingAgent()
        self.email_agent = EmailAgent()

    def run(self):

        # Fetch articles from RSS feeds
        scraped_items = self.rss_scraper.run()

        # Determine today's article table
        table_name = self.repo.get_today_table()

        for item in scraped_items[:15]:

            print(f"[Pipeline] Processing: {item['title']}")

            # Extract full article text
            raw_text = self.extractor.extract(item["link"])

            # Generate summarized version
            summary = self.summarizer_agent.run(raw_text)

            article = {
                "title": item["title"],
                "link": item["link"],
                "summary": summary,
            }

            # Compute semantic similarity score
            score = self.ranking_agent.score(article)

            # Store article in database (insert or update)
            self.repo.upsert_article(
                table_name=table_name,
                article=article,
                score=score,
                published_raw=item.get("published"),
            )

        print("[Pipeline] Fetching top ranked articles...")

        # Fetch top ranked articles for newsletter
        top_articles = self.repo.fetch_top_articles(table_name)

        # Send newsletter email
        self.email_agent.send(top_articles)

        print("[Pipeline] Completed.")