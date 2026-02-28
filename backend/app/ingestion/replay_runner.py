from .csv_parser import parse_csv
from ..models.signal import Signal
from ..database import SessionLocal


def run_replay(csv_path: str, user_id):
    # Lazy import to avoid circular dependency
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    import main
    core_engine = main.smc_engine
    
    rows = parse_csv(csv_path)

    db = SessionLocal()

    for row in rows:
        result = core_engine.process(row)

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
