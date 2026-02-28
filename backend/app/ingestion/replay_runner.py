from app.ingestion.csv_parser import parse_csv
from core_engine import smc_engine as core_engine
from app.models.signal import Signal
from app.database import SessionLocal


def run_replay(csv_path: str, user_id):
    rows = parse_csv(csv_path)

    db = SessionLocal()

    for row in rows:
        result = core_engine.on_bar(row)

        if result and result.get("signal"):
            signal = Signal(
                user_id=user_id,
                direction=result["direction"],
                entry_price=result["price"],
                timestamp=row["ts"]
            )
            db.add(signal)

    db.commit()
    db.close()
