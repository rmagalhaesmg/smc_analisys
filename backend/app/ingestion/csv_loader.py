import pandas as pd
from app.ingestion.schemas import ProfitCSVRow

def load_profit_csv(path: str):
    df = pd.read_csv(path)
    rows = []

    for _, r in df.iterrows():
        rows.append(
            ProfitCSVRow(
                timestamp=r["timestamp"],
                open=r["open"],
                high=r["high"],
                low=r["low"],
                close=r["close"],
                volume=r["volume"],
                delta=r["delta"],
                trades=r["trades"]
            )
        )
    return rows
