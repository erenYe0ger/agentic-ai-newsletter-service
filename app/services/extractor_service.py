import requests
from bs4 import BeautifulSoup

class ExtractorService:
    def extract(self, url: str):
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = "\n".join([p.get_text() for p in paragraphs])
        return text.strip()