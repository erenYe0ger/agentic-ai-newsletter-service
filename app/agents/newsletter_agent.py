from app.db.session import SessionLocal
from app.db.models import Article
from app.services.extractor_service import ExtractorService
from app.agents.scraping_agent import ScrapingAgent
from app.agents.summarization_agent import SummarizationAgent
from app.agents.ranking_agent import RankingAgent
from app.agents.email_agent import EmailAgent
from app.user.profile import USER_PROFILE
import os

class NewsletterAgent:
    def run(self):
        db = SessionLocal()

        scrape = ScrapingAgent().run()
        extractor = ExtractorService()
        summarizer = SummarizationAgent()
        rank_agent = RankingAgent(USER_PROFILE["interests"])

        processed = []

        for item in scrape[:10]:
            print(f"[Pipeline] Processing: {item['title']}")

            raw = extractor.extract(item["link"])
            summary = summarizer.run(raw)

            article = {
                "title": item["title"],
                "link": item["link"],
                "summary": summary,
                "full_text": raw,
            }

            score = rank_agent.score(article)
            article["score"] = score

            # Skip duplicates
            exists = db.query(Article).filter_by(link=item["link"]).first()
            if exists:
                print("[Pipeline] Skipping duplicate:", item["title"])
                continue

            db_obj = Article(
                title=article["title"],
                link=article["link"],
                full_text=raw,
                summary=summary
            )
            db.add(db_obj)
            db.commit()

            processed.append(article)

        processed.sort(key=lambda x: x["score"], reverse=True)
        top5 = processed[:5]

        EmailAgent().send(top5)

        print("[NewsletterAgent] Completed.")