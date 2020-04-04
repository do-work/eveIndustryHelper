import os

from dotenv import load_dotenv


class Config:
    load_dotenv("./config/.env")

    APP_PORT = os.getenv("APP_PORT", 9001)
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    CLIENT_ID = os.getenv("CLIENT_ID")
    LOGIN_SERVER_BASE = os.getenv("LOGIN_SERVER_BASE")
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
    SERVER_NAME = os.getenv("SERVER_NAME")

    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
