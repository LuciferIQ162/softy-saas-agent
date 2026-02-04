import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from backend directory so it works regardless of cwd
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")