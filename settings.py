import os

from dotenv import load_dotenv
load_dotenv()

CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
LOGIN_SERVER_BASE = os.getenv("LOGIN_SERVER_BASE")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
