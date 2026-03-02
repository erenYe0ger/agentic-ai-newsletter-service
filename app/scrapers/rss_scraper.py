import feedparser
from datetime import datetime, timedelta, timezone

class RSSScraper:
    FEED_URL = "https://techcrunch.com/feed/"

    def get_last_24h_articles(self):
        feed = feedparser.parse(self.FEED_URL)
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(hours=24)

        articles = []
        for entry in feed.entries:
            published = None
            if hasattr(entry, "published_parsed"):
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

            if published and published > cutoff:
                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published_at": published
                })

        return articles