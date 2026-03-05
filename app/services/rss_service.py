import feedparser
from bs4 import BeautifulSoup
from typing import Any


class RSSService:
    """
    Generic RSS reader.

    Fetches articles from a feed and returns normalized
    article dictionaries so the pipeline stays source-agnostic.
    """

    def fetch(self, url: str) -> list[dict[str, Any]]:

        feed: Any = feedparser.parse(url)

        articles: list[dict[str, Any]] = []

        for entry in feed.entries:

            # RSS descriptions often contain HTML → remove tags
            raw_description: str = entry.get("description", "")
            clean_description: str = BeautifulSoup(
                raw_description, "html.parser"
            ).get_text()

            articles.append({
                "title": entry.get("title"),
                "link": entry.get("link"),

                # Different feeds use different date fields
                "published": entry.get("published") or entry.get("pubDate"),

                # Optional short description
                "description": clean_description
            })

        return articles