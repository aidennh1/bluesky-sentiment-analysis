import sqlite3
import os

def init_db(path: str = "data/sentiment.db") -> sqlite3.Connection:
    """
    Initialize the SQLite database, creating the posts table if needed.

    Args:
        path: Path to the SQLite file. Parent directory is created if missing.

    Returns:
        An open sqlite3 Connection.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker      TEXT,
            text        TEXT,
            score       REAL,
            created_at  TEXT
        )
    """)
    conn.commit()
    return conn

def save_results(conn: sqlite3.Connection, ticker: str, posts: list[dict]):
    """
    Insert scored posts for a ticker into the database.

    Args:
        conn: Open SQLite connection from init_db().
        ticker: Ticker symbol these posts belong to.
        posts: List of scored post dicts with keys text, score, created_at.
    """
    conn.executemany(
        "INSERT INTO posts (ticker, text, score, created_at) VALUES (?, ?, ?, ?)",
        [(ticker, p["text"], p["score"], p["created_at"]) for p in posts]
    )
    conn.commit()