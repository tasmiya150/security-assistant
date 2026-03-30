import sqlite3
from pathlib import Path

DB_PATH = Path("data/security.db")

def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password_hash TEXT NOT NULL,
            strength TEXT NOT NULL,
            score INTEGER NOT NULL,
            checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_check(password_hash: str, strength: str, score: int):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO checks (password_hash, strength, score) VALUES (?, ?, ?)",
        (password_hash, strength, score)
    )
    conn.commit()
    conn.close()

def get_recent_checks(limit: int = 10) -> list:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT strength, score, checked_at FROM checks ORDER BY checked_at DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [{"strength": r[0], "score": r[1], "checked_at": r[2]} for r in rows]