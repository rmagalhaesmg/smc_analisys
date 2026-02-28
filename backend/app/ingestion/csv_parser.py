import pandas as pd

def parse_csv(path):
    df = pd.read_csv(path)
    for _, r in df.iterrows():
        yield {
            "ts": r["timestamp"],
            "open": r["open"],
            "high": r["high"],
            "low": r["low"],
            "close": r["close"],
            "volume": r["volume"],
            "delta": r["delta"],
            "trades": r["trades"]
        }
