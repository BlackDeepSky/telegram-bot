from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")