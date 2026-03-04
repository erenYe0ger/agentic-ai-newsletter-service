from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

class SummarizerService:
    def __init__(self):
        self.client = InferenceClient(api_key=os.getenv("HF_API_TOKEN"))

        # load model list from config
        with open("app/config/models.json", "r") as f:
            data = json.load(f)
        self.models = data["models"]

    def summarize(self, text: str):

        messages = [
            {"role": "system", "content": "You summarize articles in 4-5 lines."},
            {"role": "user", "content": text},
        ]

        for model in self.models:
            try:
                print(f"[Summarizer] Trying model: {model}")

                out = self.client.chat_completion(
                    model=model,
                    messages=messages,
                    max_tokens=200,
                )

                summary = out.choices[0].message.content.strip()

                if summary:
                    print(f"[Summarizer] Success with {model}")
                    return summary

            except Exception as e:
                print(f"[Summarizer] Failed with {model}")
                continue

        # if all models fail
        return "Summary unavailable."