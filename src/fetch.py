import re
from atproto import Client


def fetch_posts(
    client: Client,
    ticker_list: list[str],
    limit_per_ticker: int = 500,
):
    for ticker in ticker_list:
        try:
            response = client.app.bsky.feed.search_posts({
                "q": f"${ticker}",
                "limit": limit_per_ticker,
            })

            ticker_re = re.compile(
                rf"\${re.escape(ticker)}\b",
                re.IGNORECASE,
            )

            for post in response.posts:
                text = getattr(post.record, "text", "")
                langs = getattr(post.record, "langs", [])
                created_at = getattr(post.record, "created_at", None)

                if not text:
                    continue

                if "en" not in langs:
                    continue

                if not ticker_re.search(text):
                    continue

                yield (
                    ticker.upper(),  
                    text,          
                    created_at,      
                )

        except Exception as e:
            print(f"Failed to fetch {ticker}: {e}")