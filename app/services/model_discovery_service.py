import requests
import os
from dotenv import load_dotenv

load_dotenv()


class ModelDiscoveryService:
    """
    Discovers available HuggingFace inference models at runtime
    and returns only chat-capable LLMs suitable for summarization.
    """

    def __init__(self):
        self.hf_token = os.getenv("HF_API_TOKEN")
        self.url = "https://router.huggingface.co/v1/models"

        # Keywords indicating instruction/chat-tuned models
        self.keywords = ["instruct", "chat", "it"]

    def fetch_models(self) -> list[str]:
        """Fetch models from HF router and filter usable ones."""

        headers = {"Authorization": f"Bearer {self.hf_token}"}
        response = requests.get(self.url, headers=headers, timeout=20)

        if response.status_code != 200:
            raise RuntimeError("Failed to fetch HF models")

        data = response.json().get("data", [])

        # Keep only models likely to support chat completion
        models = [
            m["id"]
            for m in data
            if any(k in m["id"].lower() for k in self.keywords)
        ]

        # Limit list to avoid long fallback loops
        return models[:25]