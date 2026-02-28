def normalize(row):
    return {
        "ts": row.timestamp,
        "ohlc": (row.open, row.high, row.low, row.close),
        "volume": row.volume,
        "delta": row.delta,
        "trades": row.trades
    }
