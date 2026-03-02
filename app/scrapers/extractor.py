import httpx
import trafilatura

class ArticleExtractor:
    @staticmethod
    def extract(url: str) -> str:
        response = httpx.get(url, timeout=20)
        response.raise_for_status()

        extracted = trafilatura.extract(
            response.text,
            include_comments=False,
            include_tables=False
        )

        return extracted or ""