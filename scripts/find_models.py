import requests
import os
from dotenv import load_dotenv

load_dotenv()

hf_token = os.getenv("HF_API_TOKEN")

url = "https://router.huggingface.co/v1/models"
headers = {"Authorization": f"Bearer {hf_token}"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    models = response.json().get("data", [])

    print(f"\nFound {len(models)} available models:\n")

    for m in models:
        print(m["id"])

else:
    print("Failed to fetch models")
    print(response.text)