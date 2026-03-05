import requests
import os
from dotenv import load_dotenv
from typing import Any

load_dotenv()


class ModelDiscoveryService:
    """
    Discovers available HuggingFace inference models at runtime
    and returns only chat-capable LLMs suitable for summarization.
    """

    def __init__(self) -> None:
        self.hf_token: str | None = os.getenv("HF_API_TOKEN")
        self.url: str = "https://router.huggingface.co/v1/models"

        # Keywords indicating instruction/chat-tuned models
        self.keywords: list[str] = ["instruct", "chat", "it"]

    def fetch_models(self) -> list[str]:
        """Fetch models from HF router and filter usable ones."""

        headers: dict[str, str] = {"Authorization": f"Bearer {self.hf_token}"}
        response: requests.Response = requests.get(self.url, headers=headers, timeout=20)

        if response.status_code != 200:
            raise RuntimeError("Failed to fetch HF models")

        data: list[dict[str, Any]] = response.json().get("data", [])

        # Keep only models likely to support chat completion
        models: list[str] = [
            m["id"]
            for m in data
            if any(k in m["id"].lower() for k in self.keywords)
        ]

        # Limit list to avoid long fallback loops
        return models[:25]