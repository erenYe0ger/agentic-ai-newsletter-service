import os
import warnings
from transformers.utils import logging

warnings.filterwarnings("ignore")

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

logging.set_verbosity_error()

from app.agents.newsletter_agent import NewsletterAgent

if __name__ == "__main__":
    NewsletterAgent().run()