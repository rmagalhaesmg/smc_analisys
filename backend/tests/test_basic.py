import sys
from pathlib import Path
# ensure workspace root on path so "app" package is importable
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from backend.main import app, Candle

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "app" in r.json()

def test_metrics():
    r = client.get("/metrics")
    # metrics may not be implemented if prometheus_client not installed
    assert r.status_code in (200, 501)
    if r.status_code == 200:
        assert "smc_requests_total" in r.text

def test_candle_validation():
    # valid candle
    c = {
        "timestamp": "10:00",
        "open": 1,
        "high": 2,
        "low": 1,
        "close": 1.5,
        "volume": 100
    }
    r = client.post("/analyze/candle", json=c)
    assert r.status_code == 200
    assert r.json()["status"] == "queued"

    # invalid candle missing field
    bad = {"timestamp": "10:00", "open": 1}
    r = client.post("/analyze/candle", json=bad)
    assert r.status_code == 422
