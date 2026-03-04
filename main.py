import subprocess
import sys
import time
import warnings
import os
from transformers.utils import logging

# Silence unnecessary warnings
warnings.filterwarnings("ignore")

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

logging.set_verbosity_error()


def log(msg: str):
    print(f"\n[ 🟦 {msg} ]\n")


def run(cmd: str):
    try:
        subprocess.run(
            cmd,
            shell=True,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {cmd}")
        print(e)
        sys.exit(1)


def main():

    log("STEP 1 — Starting Docker Postgres")
    run("docker compose -f docker/docker-compose.yml up -d")

    time.sleep(2)

    log("STEP 2 — Initializing Database Tables")
    run("uv run app/db/init_db.py")

    log("STEP 3 — Running Newsletter Pipeline")

    from app.agents.orchestrator import Orchestrator

    Orchestrator().run()

    log("🎉 DONE — Newsletter Pipeline Completed Successfully!")


if __name__ == "__main__":
    main()