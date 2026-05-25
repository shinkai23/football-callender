import os

from dotenv import load_dotenv

load_dotenv()

FOOTBALL_API_BASE_URL = os.getenv("FOOTBALL_API_BASE_URL", "https://api.football-data.org/v4",)
FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY", "")
