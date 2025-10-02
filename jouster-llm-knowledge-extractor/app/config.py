
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SUMMARY_SENTENCE_MAX = 2
TOPIC_COUNT = 3
KEYWORD_COUNT = 3
