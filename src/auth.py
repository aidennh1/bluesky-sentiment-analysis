import os
from dotenv import load_dotenv
from atproto import Client

def get_client() -> Client:
    """Load credentials from .env and return an authenticated Bluesky client."""
    load_dotenv()
    client = Client()
    client.login(os.getenv("USER"), os.getenv("PASSWORD"))
    return client