import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","")
OPENAI_MODEL_MAIN = os.getenv("OPENAI_MODEL_MAIN","gpt-4o-2024-08-06")
OPENAI_MODEL_LITE = os.getenv("OPENAI_MODEL_LITE","gpt-4o-mini")
OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL","text-embedding-3-large")

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY","")
EDAMAM_APP_ID = os.getenv("EDAMAM_APP_ID","")
EDAMAM_APP_KEY = os.getenv("EDAMAM_APP_KEY","")

# YouTube integration (optional)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY","")

SMTP_HOST = os.getenv("SMTP_HOST","")
SMTP_PORT = int(os.getenv("SMTP_PORT","587"))
SMTP_USER = os.getenv("SMTP_USER","")
SMTP_PASS = os.getenv("SMTP_PASS","")
EMAIL_FROM = os.getenv("EMAIL_FROM","Nigela <noreply@example.com>")
EMAIL_TO = os.getenv("EMAIL_TO","").strip()
TIMEZONE = os.getenv("TIMEZONE","Asia/Kolkata")
