from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()


class SummarizerService:
    """
    Service responsible for generating article summaries
    using HuggingFace Inference API.

    Implements automatic model fallback if a model fails.
    """

    def __init__(self):

        self.client = InferenceClient(
            api_key=os.getenv("HF_API_TOKEN")
        )

        from app.services.model_discovery_service import ModelDiscoveryService
        self.models = ModelDiscoveryService().fetch_models()

    def summarize(self, text: str) -> str:
        """
        Generate a short summary of the article.

        Ensures consistent fallback behavior:
        If the model cannot summarize, returns:
        'Summary unavailable.'
        """

        messages = [
            {
                "role": "system",
                "content": (
                    "You are summarizing a tech news article for a newsletter.\n\n"
                    "Generate a concise 2-3 sentence summary.\n\n"
                    "Rules:\n"
                    "- Use only the provided content.\n"
                    "- Do NOT add introductions like 'Here is the summary'.\n"
                    "- Do NOT use bullet points.\n"
                    "- Write plain sentences suitable for a newsletter.\n\n"
                    "If the article content is missing or unclear, "
                    "return exactly this text:\n"
                    "Summary unavailable."
                )
            },
            {
                "role": "user",
                "content": text
            },
        ]

        for model in self.models:
            try:

                out = self.client.chat_completion(
                    model=model,
                    messages=messages,
                    max_tokens=200,
                    temperature=0.2,
                )

                summary = out.choices[0].message.content.strip()

                if not summary:
                    continue

                lower = summary.lower()

                # Force consistent fallback
                if (
                    "no article provided" in lower
                    or "no content" in lower
                    or "not enough information" in lower
                    or "cannot summarize" in lower
                ):
                    return "Summary unavailable."

                return summary

            except Exception:
                continue

        return "Summary unavailable."