import os
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE_PATH = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(ENV_FILE_PATH)

FOOTBALL_API_BASE_URL = os.getenv(
    "FOOTBALL_API_BASE_URL",
    "https://api.football-data.org/v4",
).rstrip("/")
FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY", "")
