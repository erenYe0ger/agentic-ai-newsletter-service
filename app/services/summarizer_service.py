from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import json

load_dotenv()


class SummarizerService:

    def __init__(self):
        self.client = InferenceClient(api_key=os.getenv("HF_API_TOKEN"))

        # Load model list dynamically
        with open("app/config/models.json", "r") as f:
            data = json.load(f)

        self.models = data["models"]

    def summarize(self, text: str):

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
                continue

        # fallback if all models fail
        return "Summary unavailable."