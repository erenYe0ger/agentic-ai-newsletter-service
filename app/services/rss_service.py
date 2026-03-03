import feedparser

class RSSService:
    def fetch(self, url: str):
        feed = feedparser.parse(url)
        articles = []

        for e in feed.entries:
            articles.append({
                "title": e.title,
                "link": e.link,
                "published": e.get("published", None)
            })
        return articles