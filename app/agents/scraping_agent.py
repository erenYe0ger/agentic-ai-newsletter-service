from app.services.rss_service import RSSService

class ScrapingAgent:
    def run(self):
        print("[ScrapingAgent] Fetching RSS...")
        rss = RSSService()
        return rss.fetch("https://techcrunch.com/feed/")