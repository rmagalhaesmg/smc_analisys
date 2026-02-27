from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random

app = FastAPI(title="SMC Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "SMC API running"}

@app.get("/api/signals")
def get_signals():
    # placeholder - conectar com seu engine depois
    return {"signals": [
        {"id": 1, "type": "BOS", "price": 5210.50, "score": 0.87, "timestamp": datetime.now().isoformat()},
        {"id": 2, "type": "CHoCH", "price": 5198.00, "score": 0.72, "timestamp": datetime.now().isoformat()},
    ]}

@app.get("/api/candles")
def get_candles():
    # placeholder
    candles = []
    price = 5200.0
    for i in range(50):
        open_ = price
        close = price + random.uniform(-10, 10)
        high = max(open_, close) + random.uniform(0, 5)
        low = min(open_, close) - random.uniform(0, 5)
        candles.append({"time": i, "open": open_, "high": high, "low": low, "close": close})
        price = close
    return {"candles": candles}

@app.get("/api/alerts")
def get_alerts():
    return {"alerts": [
        {"id": 1, "message": "BOS detectado em 5210", "level": "high", "timestamp": datetime.now().isoformat()},
        {"id": 2, "message": "Liquidez acumulada em 5190", "level": "medium", "timestamp": datetime.now().isoformat()},
    ]}

@app.get("/api/status")
def get_status():
    return {"engine": "online", "signals_today": 12, "win_rate": 0.73, "uptime": "99.9%"}