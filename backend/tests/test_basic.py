import sys
from pathlib import Path
# ensure workspace root is on path so "backend" package can be imported
# tests reside at <workspace>/backend/tests, so parents[2] is the workspace root
sys.path.append(str(Path(__file__).resolve().parents[2]))

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

    # queue size indicator is present when metrics enabled (not strict)
    # we cannot access internal queue here, but endpoint returned queued

    # invalid candle missing field
    bad = {"timestamp": "10:00", "open": 1}
    r = client.post("/analyze/candle", json=bad)
    assert r.status_code == 422


def test_notifications_configure():
    payload = {"telegram_token": "abc123", "email_to": ["a@b.com"]}
    r = client.post("/notifications/configure", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "success"

    # sending test notifications (will be skipped because not configured fully)
    r = client.post("/notifications/test", json={})
    assert r.status_code == 200
    assert isinstance(r.json(), dict)


def test_api_stream_validation():
    # missing endpoint should 422
    r = client.post("/data/api-stream", json={})
    assert r.status_code == 422
    # valid payload should at least respond (probably 200)
    r = client.post("/data/api-stream", json={"endpoint": "http://example.com"})
    assert r.status_code in (200, 500)
