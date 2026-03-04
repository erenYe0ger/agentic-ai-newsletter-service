from app.services.rss_service import RSSService


class RSSScraperAgent:
    """
    Agent responsible for collecting article metadata
    from configured RSS feeds.
    """

    def __init__(self):
        self.rss = RSSService()

    def run(self) -> list[dict]:
        print("[RSSScraperAgent] Fetching RSS feeds...")

        sources = [
            "https://techcrunch.com/feed/",
            # future feeds go here
        ]

        articles = []

        for url in sources:
            articles.extend(self.rss.fetch(url))

        return articles