import requests
import os
from dotenv import load_dotenv
from atproto import Client


def main():
    load_dotenv()
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")

    client = Client()  
    client.login(user,password)

if __name__ == '__main__':
    main()