import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_API_TOKEN")

class ModelDiscoveryService:

    URL = "https://router.huggingface.co/v1/models"

    KEYWORDS = [
        "instruct",
        "chat",
        "it",
    ]

    def fetch_models(self):
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        r = requests.get(self.URL, headers=headers, timeout=20)

        if r.status_code != 200:
            print("HF model fetch failed")
            return []

        data = r.json().get("data", [])

        models = []

        for m in data:
            mid = m["id"].lower()

            if any(k in mid for k in self.KEYWORDS):
                models.append(m["id"])

        return models

    def save_models(self, path="app/config/models.json"):
        models = self.fetch_models()

        if not models:
            print("No models discovered")
            return

        os.makedirs("app/config", exist_ok=True)

        with open(path, "w") as f:
            json.dump({"models": models}, f, indent=2)

        print(f"Saved {len(models)} models to {path}")