import os
from dotenv import load_dotenv

load_dotenv()

MINJUST_BASE_URL = "https://cbd.minjust.gov.kg/api/v1"
MINJUST_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
}

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")