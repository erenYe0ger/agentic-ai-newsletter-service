from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()


class SummarizerService:
    """
    Service responsible for generating article summaries
    using HuggingFace Inference API.

    Implements automatic model fallback if a model fails.
    """

    def __init__(self):

        # Initialize HuggingFace inference client
        self.client = InferenceClient(
            api_key=os.getenv("HF_API_TOKEN")
        )

        from app.services.model_discovery_service import ModelDiscoveryService

        self.models = ModelDiscoveryService().fetch_models()

    def summarize(self, text: str) -> str:
        """
        Generate a short summary of the article.

        Tries multiple models sequentially until one succeeds.
        """

        messages = [
            {
                "role": "system",
                "content": (
                    "Summarize the following tech news article in 2-3 concise sentences. "
                    "Write directly in plain sentences suitable for a newsletter. "
                    "Do NOT include introductions like 'Here is the summary', "
                    "'Summary:', or similar phrases. "
                    "Do NOT include bullet points or headings."
                )
            },
            {
                "role": "user",
                "content": text
            },
        ]

        # Try each model until one succeeds
        for model in self.models:
            try:

                out = self.client.chat_completion(
                    model=model,
                    messages=messages,
                    max_tokens=200,
                    temperature=0.2,
                )

                summary = out.choices[0].message.content.strip()

                if summary:
                    return summary

            except Exception:
                # silently fallback to next model
                continue

        # If all models fail
        return "Summary unavailable."