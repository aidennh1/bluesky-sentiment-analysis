from auth import get_client
from fetch import fetch_posts

def main():

    client = get_client()
    posts = fetch_posts(client, "NVDA")
    for i in range(3):
        print(posts[i])
        print()
if __name__ == '__main__':
    main()