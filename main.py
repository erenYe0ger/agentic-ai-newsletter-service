import warnings
import os
from transformers.utils import logging

from app.db.init_db import init_db
from app.agents.orchestrator import Orchestrator


# Silence unnecessary warnings
warnings.filterwarnings("ignore")

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

logging.set_verbosity_error()


def log(msg: str) -> None:
    print(f"\n[ 🟦 {msg} ]\n", flush=True)


def main() -> None:

    # Ensure required tables exist
    log("Initializing Database Tables")
    init_db()

    # Run newsletter pipeline
    log("Running Newsletter Pipeline")
    Orchestrator().run()

    log("🎉 DONE — Newsletter Pipeline Completed Successfully!")


if __name__ == "__main__":
    main()