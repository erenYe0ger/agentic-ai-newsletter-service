from app.db.session import SessionLocal
from sqlalchemy import text
from email.utils import parsedate_to_datetime
from app.services.extractor_service import ExtractorService
from app.agents.scraping_agent import ScrapingAgent
from app.agents.summarization_agent import SummarizationAgent
from app.agents.ranking_agent import RankingAgent
from app.agents.email_agent import EmailAgent
import datetime


class NewsletterAgent:

    def run(self):

        db = SessionLocal()

        scraper = ScrapingAgent()
        extractor = ExtractorService()
        summarizer = SummarizationAgent()
        rank_agent = RankingAgent()

        scraped_items = scraper.run()

        today = datetime.datetime.now(datetime.UTC).strftime("%d_%m_%Y")
        table_name = f"articles_{today}"

        for item in scraped_items[:15]:

            print(f"[Pipeline] Processing: {item['title']}")

            raw_text = extractor.extract(item["link"])

            summary = summarizer.run(raw_text)

            article = {
                "title": item["title"],
                "link": item["link"],
                "summary": summary,
            }

            score = rank_agent.score(article)

            published_raw = item.get("published")

            try:
                published = parsedate_to_datetime(published_raw)
            except Exception:
                published = None

            exists = db.execute(
                text(f"SELECT id FROM {table_name} WHERE link=:link"),
                {"link": article["link"]}
            ).fetchone()

            if exists:

                db.execute(
                    text(f"""
                    UPDATE {table_name}
                    SET
                        title=:title,
                        summary=:summary,
                        similarity_score=:score,
                        published_at=:published
                    WHERE link=:link
                    """),
                    {
                        "title": article["title"],
                        "summary": summary,
                        "score": score,
                        "published": published,
                        "link": article["link"]
                    }
                )

                db.commit()

                print("[Pipeline] Updated existing article")

            else:

                db.execute(
                    text(f"""
                    INSERT INTO {table_name}
                    (title, link, summary, similarity_score, published_at)
                    VALUES (:title, :link, :summary, :score, :published)
                    """),
                    {
                        "title": article["title"],
                        "link": article["link"],
                        "summary": summary,
                        "score": score,
                        "published": published
                    }
                )

                db.commit()

        print("[Pipeline] Fetching top ranked articles...")

        rows = db.execute(
            text(f"""
                SELECT title, link, summary
                FROM {table_name}
                WHERE summary != 'Summary unavailable.'
                ORDER BY similarity_score DESC
                LIMIT 5
            """)
        ).fetchall()

        top5 = [
            {
                "title": r[0],
                "link": r[1],
                "summary": r[2]
            }
            for r in rows
        ]

        EmailAgent().send(top5)

        print("[NewsletterAgent] Completed.")