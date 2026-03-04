import requests
from bs4 import BeautifulSoup


class ExtractorService:
    """
    Service responsible for extracting article text
    from a given webpage URL.
    """

    def extract(self, url: str) -> str:

        response = requests.get(url, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")

        text = "\n".join(p.get_text() for p in paragraphs)

        return text.strip()