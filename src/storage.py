import sqlite3

def init_db(path: str = "data/sentiment.db") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            text TEXT,
            score REAL,
            created_at TEXT
        )
    """)
    conn.commit()
    return conn

def save_results(conn: sqlite3.Connection, ticker: str, posts: list[dict]):
    conn.executemany(
        "INSERT INTO posts (ticker, text, score, created_at) VALUES (?, ?, ?, ?)",
        [(ticker, p["text"], p["score"], p["created_at"]) for p in posts]
    )
    conn.commit()