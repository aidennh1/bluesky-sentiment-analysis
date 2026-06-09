import sqlite3
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def plot_ticker(ticker: str, days: int = 30):
    conn = sqlite3.connect("data/sentiment.db")
    df = pd.read_sql(
        "SELECT date(created_at) as date, AVG(score) as sentiment FROM posts WHERE ticker=? GROUP BY date(created_at)",
        conn, params=(ticker,)
    )
    df["date"] = pd.to_datetime(df["date"])

    price = yf.download(ticker, period=f"{days}d", interval="1d")[["Close"]].reset_index()
    price.columns = ["date", "price"]

    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax2 = ax1.twinx()

    ax1.plot(price["date"], price["price"], color="steelblue", label="Price")
    ax2.bar(df["date"], df["sentiment"], alpha=0.4, color="green", label="Sentiment")

    ax1.set_ylabel("Price ($)")
    ax2.set_ylabel("Avg Sentiment")
    ax1.set_xlabel("Date")
    plt.title(f"{ticker} — Price vs Bluesky Sentiment")
    fig.tight_layout()
    plt.savefig(f"data/{ticker}_sentiment.png")
    plt.show()