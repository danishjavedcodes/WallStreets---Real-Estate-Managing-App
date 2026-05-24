import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-wallstreets-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:sys@localhost:5432/Wall-Street-Admin",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    PORT = int(os.getenv("PORT", "5001"))
