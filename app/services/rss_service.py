import feedparser


class RSSService:
    """
    Service responsible for fetching and parsing RSS feeds.
    """

    def fetch(self, url: str) -> list[dict]:

        feed = feedparser.parse(url)

        articles = []

        for e in feed.entries:
            articles.append({
                "title": e.title,
                "link": e.link,
                "published": e.get("published", None),
            })

        return articles