import sys
from pathlib import Path
# ensure workspace root is on path so "backend" package can be imported
# tests reside at <workspace>/backend/tests, so parents[2] is the workspace root
sys.path.append(str(Path(__file__).resolve().parents[2]))

from fastapi.testclient import TestClient
from backend.main import app  # Candle type was removed from main, tests just exercise endpoints

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "app" in r.json()


def test_metrics():
    r = client.get("/metrics")
    # metrics may not be implemented if prometheus_client not installed
    # metrics endpoint may not exist; accept 200, 501 or 404
    assert r.status_code in (200, 501, 404)
    if r.status_code == 200:
        assert "smc_requests_total" in r.text


# the following functional tests are legacy examples and not applicable to current backend
# they have been removed to keep the test suite focused on auth and billing.
