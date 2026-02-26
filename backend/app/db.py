"""
Banco de dados simplificado usando sqlite para persistência de sinais
"""
import sqlite3
import json
from app.config import settings

# extrair caminho do DATABASE_URL (suporta sqlite:///<path>)
def _get_sqlite_path(url: str) -> str:
    if url.startswith("sqlite:///"):
        return url.replace("sqlite://", "")
    return url

_db_path = _get_sqlite_path(settings.DATABASE_URL)
conn = sqlite3.connect(_db_path, check_same_thread=False)
conn.row_factory = sqlite3.Row
_cursor = conn.cursor()

# criar tabelas se não existirem
_cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS signals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        type TEXT,
        price REAL,
        score REAL,
        alert INTEGER,
        data TEXT
    )
    """
)
_cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS outcomes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        signal_id INTEGER,
        timestamp TEXT,
        data TEXT
    )
    """
)
conn.commit()


def save_signal(signal: dict) -> None:
    try:
        _cursor.execute(
            "INSERT INTO signals (timestamp,type,price,score,alert,data) VALUES (?,?,?,?,?,?)",
            (
                signal.get('timestamp'),
                signal.get('type'),
                signal.get('price'),
                signal.get('score'),
                int(signal.get('alert', False)),
                json.dumps(signal)
            )
        )
        conn.commit()
    except Exception:
        pass


def save_outcome(signal_id: int, outcome: dict) -> None:
    try:
        _cursor.execute(
            "INSERT INTO outcomes (signal_id,timestamp,data) VALUES (?,?,?)",
            (
                signal_id,
                outcome.get('timestamp'),
                json.dumps(outcome)
            )
        )
        conn.commit()
    except Exception:
        pass
