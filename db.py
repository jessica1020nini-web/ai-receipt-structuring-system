import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path("receipts.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merchant TEXT NOT NULL,
            date TEXT NOT NULL,
            total REAL NOT NULL,
            created_at TEXT NOT NULL,
            source_image TEXT,
            dedup_key TEXT UNIQUE
        )
        """)
        conn.commit()

def insert_receipt(r: Dict[str, Any]) -> bool:
    """
    Returns True if inserted, False if duplicate (dedup_key conflict)
    """
    init_db()
    with get_conn() as conn:
        try:
            conn.execute(
                """
                INSERT INTO receipts (merchant, date, total, created_at, source_image, dedup_key)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    r.get("merchant", ""),
                    r.get("date", ""),
                    float(r.get("total", 0)),
                    r.get("created_at", ""),
                    r.get("source_image", None),
                    r.get("dedup_key", None),
                ),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def list_receipts() -> List[Dict[str, Any]]:
    init_db()
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM receipts ORDER BY id DESC").fetchall()
        return [dict(row) for row in rows]

def total_expense() -> float:
    init_db()
    with get_conn() as conn:
        row = conn.execute("SELECT COALESCE(SUM(total), 0) AS s FROM receipts").fetchone()
        return float(row["s"])