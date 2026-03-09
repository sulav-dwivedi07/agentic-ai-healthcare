import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Go 3 levels up:
# config.py → utils → src → backend
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "data",
    "raw",
    "indian_healthcare_master.csv"
)

MODEL_PRIORITY = [
    "gemini-3-flash",      # Newest, likely has 20/20 requests left
    "gemini-1.5-flash-8b", # Faster, lighter, often has its own separate quota
    "gemini-2.5-flash-lite" # Another efficient alternative
]