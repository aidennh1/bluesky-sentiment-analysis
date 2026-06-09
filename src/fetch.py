import re
from atproto import Client

def fetch_posts(
    client: Client,
    ticker_list: list[str],
    limit_per_ticker: int = 100,
):
    """
    Fetch Bluesky posts mentioning each ticker and yield filtered results.

    Searches for posts containing $TICKER, filters to English-language posts
    that explicitly match the ticker pattern, and yields a tuple per post.

    Args:
        client: Authenticated atproto Client instance.
        ticker_list: List of ticker symbols to search e.g. ["NVDA", "AAPL"].
        limit_per_ticker: Max posts to request per ticker (API cap is 100).

    Yields:
        Tuple of (ticker, text, created_at) for each matching post.
    """
    for ticker in ticker_list:
        try:
            response = client.app.bsky.feed.search_posts({
                "q": f"${ticker}",
                "limit": limit_per_ticker,
            })

            # match $TICKER with a word boundary, case-insensitive
            ticker_re = re.compile(rf"\${re.escape(ticker)}\b", re.IGNORECASE)

            for post in response.posts:
                text = getattr(post.record, "text", "")
                langs = getattr(post.record, "langs", [])
                created_at = getattr(post.record, "created_at", None)

                if not text:
                    continue

                # skip non-English posts
                if "en" not in langs:
                    continue

                # skip posts that don't actually mention the ticker
                if not ticker_re.search(text):
                    continue

                yield (ticker.upper(), text, created_at)

        except Exception as e:
            print(f"Failed to fetch {ticker}: {e}")