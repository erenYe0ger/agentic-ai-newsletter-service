from app.scrapers.rss_scraper import RSSScraper
from app.scrapers.extractor import ArticleExtractor
from app.services.summarizer_service import Summarizer
from app.db.session import SessionLocal
from app.db.models import Article

class PipelineService:
    def __init__(self):
        self.scraper = RSSScraper()
        self.extractor = ArticleExtractor()
        self.summarizer = Summarizer()

    def run(self):
        articles = self.scraper.get_last_24h_articles()
        if not articles:
            print("No new articles.")
            return

        db = SessionLocal()

        for a in articles:
            exists = db.query(Article).filter_by(link=a["link"]).first()
            if exists:
                continue

            full_text = self.extractor.extract(a["link"])
            if not full_text:
                print("Skipping empty extraction:", a["link"])
                continue

            summary = self.summarizer.summarize(full_text)

            row = Article(
                title=a["title"],
                link=a["link"],
                published_at=a["published_at"],
                full_text=full_text,
                summary=summary
            )

            db.add(row)
            db.commit()

            print("Inserted:", a["title"])

        db.close()