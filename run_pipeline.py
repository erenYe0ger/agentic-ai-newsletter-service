import subprocess
import sys
import time

def log(msg):
    print(f"\n[ 🟦 {msg} ]\n")


def run(cmd):
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

    log("STEP 2.5 — Updating Available HF Models")
    run("uv run scripts/update_models.py")

    log("STEP 3 — Running Full Newsletter Agent (Scrape → Extract → Summarize → Rank → Email)")
    run("uv run main.py")

    log("🎉 DONE — Newsletter Pipeline Completed Successfully!")


if __name__ == "__main__":
    main()