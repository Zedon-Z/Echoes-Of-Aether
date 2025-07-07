import os
from dotenv import load_dotenv

load_dotenv()  # Optional: loads .env when running locally

TOKEN = os.getenv("TOKEN")  # 👈 Fetches from Railway variables

MIN_PLAYERS = 6
MAX_PLAYERS = 15
NSFW_ENABLED = False
BOT_OWNER_ID = 1378500453  # Replace with your Telegram numeric user ID
