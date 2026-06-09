import sqlite3
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def plot_ticker(ticker: str, days: int = 30):
    """
    Plot price and average daily sentiment for a given ticker.

    Reads sentiment data from SQLite, fetches historical price data via
    yfinance, and saves a two-panel chart to data/<ticker>_sentiment.png.

    Args:
        ticker: Stock ticker symbol e.g. "NVDA".
        days: Number of calendar days of price history to display.
    """
    conn = sqlite3.connect("data/sentiment.db")

    # aggregate average sentiment score per day for the given ticker
    df = pd.read_sql(
        "SELECT date(created_at) as date, AVG(score) as sentiment FROM posts WHERE ticker=? GROUP BY date(created_at)",
        conn, params=(ticker,)
    )
    df["date"] = pd.to_datetime(df["date"])

    # fetch daily closing prices from yfinance
    price = yf.download(ticker, period=f"{days}d", interval="1d")[["Close"]].reset_index()
    price.columns = ["date", "price"]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # upper panel: closing price over time
    ax1.plot(price["date"], price["price"], color="steelblue", label="Price")
    ax1.set_ylabel("Price ($)")
    ax1.set_title(f"{ticker} — Price vs Bluesky Sentiment")
    ax1.legend(loc="upper left")

    # lower panel: average daily sentiment bars
    ax2.bar(df["date"], df["sentiment"], alpha=0.6, color="green", label="Avg Sentiment")
    ax2.axhline(0, color="gray", linewidth=0.8, linestyle="--")  # zero line for reference
    ax2.set_ylabel("Avg Sentiment")
    ax2.set_xlabel("Date")
    ax2.legend(loc="upper left")

    fig.tight_layout()
    plt.savefig(f"data/{ticker}_sentiment.png")
    plt.show()