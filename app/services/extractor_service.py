import requests
from bs4 import BeautifulSoup


class ExtractorService:
    """
    Extracts readable text from article webpages.
    """

    def extract(self, url: str) -> str:

        r: requests.Response = requests.get(url, timeout=10)

        soup: BeautifulSoup = BeautifulSoup(r.text, "html.parser")

        # Collect paragraph text
        paragraphs = soup.find_all("p")

        text: str = "\n".join([p.get_text() for p in paragraphs]).strip()

        return text