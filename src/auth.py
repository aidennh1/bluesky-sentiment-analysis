import os
from dotenv import load_dotenv
from atproto import Client

def get_client() -> Client:
    load_dotenv()
    client = Client()
    client.login(os.getenv("USER"), os.getenv("PASSWORD"))
    return client