import subprocess
import sys
import os
import time

def log(msg):
    print(f"\n[ 🟦 {msg} ]\n")


def run(cmd):
    """Run a shell command with real-time output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            text=True,
        )
        return result
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

    log("STEP 3 — Running Full Pipeline (Scrape → Extract → Summarize → Insert)")
    run("uv run -m app.tests.test_pipeline")

    log("🎉 DONE — Pipeline completed successfully!")


if __name__ == '__main__':
    main()