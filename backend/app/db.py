"""
app/db.py – SQLite persistence layer for SMC Web App.

The database file is always stored at:
    <project_root>/data/smc.db

where <project_root> is the directory that contains this file's parent package.
Using an absolute path means the app starts correctly regardless of the
working directory from which uvicorn / python is invoked.
"""
import sqlite3
import pathlib

# ---------------------------------------------------------------------------
# Resolve an absolute, working-directory-independent path for the DB file.
#
#   __file__  →  .../smc_analysys/backend/app/db.py
#   .parent   →  .../smc_analysys/backend/app/
#   .parent   →  .../smc_analysys/backend/          ← project root
#   / "data"  →  .../smc_analysys/backend/data/
# ---------------------------------------------------------------------------
_DB_DIR  = pathlib.Path(__file__).resolve().parent.parent / "data"
_DB_DIR.mkdir(parents=True, exist_ok=True)          # create folder if missing
_DB_PATH = _DB_DIR / "smc.db"

conn = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
cursor = conn.cursor()

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------
cursor.executescript("""
    CREATE TABLE IF NOT EXISTS signals (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at  TEXT    NOT NULL,
        signal_type TEXT    NOT NULL,
        price       REAL    NOT NULL,
        score       REAL    NOT NULL,
        regime      TEXT,
        details     TEXT
    );

    CREATE TABLE IF NOT EXISTS candles (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp   TEXT    NOT NULL,
        open        REAL    NOT NULL,
        high        REAL    NOT NULL,
        low         REAL    NOT NULL,
        close       REAL    NOT NULL,
        volume      REAL    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS ml_outcomes (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        signal_id   INTEGER REFERENCES signals(id),
        outcome     REAL,
        recorded_at TEXT
    );
""")
conn.commit()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def save_signal(signal: dict) -> int:
    """Persist a signal dict and return its rowid."""
    cursor.execute(
        """
        INSERT INTO signals (created_at, signal_type, price, score, regime, details)
        VALUES (:timestamp, :type, :price, :score, :regime, :details)
        """,
        {
            "timestamp": signal.get("timestamp", ""),
            "type":      signal.get("type", ""),
            "price":     signal.get("price", 0.0),
            "score":     signal.get("score", 0.0),
            "regime":    signal.get("regime", ""),
            "details":   str(signal.get("warnings", [])),
        },
    )
    conn.commit()
    return cursor.lastrowid


def save_outcome(signal_id: int, outcome: float) -> None:
    """Record a trade outcome for a previously saved signal."""
    from datetime import datetime, timezone
    cursor.execute(
        "INSERT INTO ml_outcomes (signal_id, outcome, recorded_at) VALUES (?, ?, ?)",
        (signal_id, outcome, datetime.now(tz=timezone.utc).isoformat()),
    )
    conn.commit()


def fetch_recent_signals(limit: int = 100) -> list:
    """Return the most recent `limit` signals as dicts."""
    cursor.execute(
        "SELECT * FROM signals ORDER BY id DESC LIMIT ?", (limit,)
    )
    cols = [d[0] for d in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]