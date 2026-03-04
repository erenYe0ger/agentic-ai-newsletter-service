from app.db.session import SessionLocal
from app.db.models import Article
from app.services.extractor_service import ExtractorService
from app.agents.scraping_agent import ScrapingAgent
from app.agents.summarization_agent import SummarizationAgent
from app.agents.ranking_agent import RankingAgent
from app.agents.email_agent import EmailAgent


class NewsletterAgent:

    def run(self):
        db = SessionLocal()

        scraper = ScrapingAgent()
        extractor = ExtractorService()
        summarizer = SummarizationAgent()
        rank_agent = RankingAgent()

        scraped_items = scraper.run()

        processed = []

        for item in scraped_items[:10]:

            print(f"[Pipeline] Processing: {item['title']}")

            # Skip duplicates first
            exists = db.query(Article).filter_by(link=item["link"]).first()
            if exists:
                print("[Pipeline] Skipping duplicate:", item["title"])
                continue

            raw_text = extractor.extract(item["link"])

            summary = summarizer.run(raw_text)

            article = {
                "title": item["title"],
                "link": item["link"],
                "summary": summary,
                "full_text": raw_text,
            }

            # store article
            db_obj = Article(
                title=article["title"],
                link=article["link"],
                full_text=raw_text,
                summary=summary
            )

            db.add(db_obj)
            db.commit()

            processed.append(article)

        # semantic ranking happens here
        ranked = rank_agent.rank(processed)

        top5 = ranked[:5]

        EmailAgent().send(top5)

        print("[NewsletterAgent] Completed.")