from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

class SummarizerService:
    def __init__(self):
        self.client = InferenceClient(api_key=os.getenv("HF_API_TOKEN"))
        self.model = "Qwen/Qwen2.5-72B-Instruct"

    def summarize(self, text: str):
        messages = [
            {"role": "system", "content": "You summarize articles in 4-5 lines."},
            {"role": "user", "content": text},
        ]

        out = self.client.chat_completion(
            model=self.model,
            messages=messages,
            max_tokens=200,
        )
        return out.choices[0].message.content.strip()