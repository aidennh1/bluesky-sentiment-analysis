from auth import get_client
from fetch import fetch_posts
from sentiment import score_posts
from storage import init_db, save_results
from chart import plot_ticker

TICKERS = ["NVDA", "AAPL", "TSLA"]

def main():
    """
    Main pipeline: authenticate, fetch posts, score sentiment,
    persist to SQLite, and render the chart for NVDA.
    """
    client = get_client()
    db = init_db()

    # fetch raw post tuples for all tickers in one pass
    raw = list(fetch_posts(client, TICKERS))

    # convert tuples to dicts for sentiment scoring
    posts = [{"text": p[1], "ticker": p[0], "created_at": p[2]} for p in raw]
    scored = score_posts(posts)

    # persist scored posts grouped by ticker
    for ticker in TICKERS:
        ticker_posts = [p for p in scored if p["ticker"] == ticker]
        save_results(db, ticker, ticker_posts)

    plot_ticker("NVDA", days=30)

if __name__ == "__main__":
    main()