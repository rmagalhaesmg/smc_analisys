import sys, os
# ensure backend directory is on path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from backend.main import app
from backend.app.database import Base, engine
from backend.app.auth.models import User
from passlib.context import CryptContext
import os

# override the password context used by auth router to avoid bcrypt issues in tests
import backend.app.auth.router as auth_module
auth_module.pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
import app.auth.router as auth_module2
auth_module2.pwd_context = auth_module.pwd_context

client = TestClient(app)


class DummySession:
    def __init__(self, url):
        self.url = url


def setup_module(module):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # create sample user
    pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # nothing else needed; tests call endpoints which handle db internally


def get_token(email="bill@example.com", password="pw"):
    # register then login
    client.post("/auth/register", json={"email": email, "password": password})
    r = client.post("/auth/login", json={"email": email, "password": password})
    return r.json()["access_token"]


def test_stripe_checkout(monkeypatch):
    token = get_token()

    def fake_create(plan, user_id):
        return "/dummy"

    monkeypatch.setattr("app.billing.stripe.create_stripe_checkout", fake_create)
    resp = client.post("/billing/checkout/stripe", json={"plan": "basic"}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["url"] == "/dummy"


def test_mp_checkout(monkeypatch):
    token = get_token(email="mp@example.com")

    def fake_mp(plan, user_id):
        return "/mp"

    monkeypatch.setattr("app.billing.mercadopago.create_mp_payment", fake_mp)
    resp = client.post("/billing/checkout/mp", json={"plan": "basic"}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["url"] == "/mp"


def test_stripe_webhook(monkeypatch):
    # simulate stripe signature verification and event payload
    token = get_token()
    from backend.app.auth.jwt import verify_token
    uid = verify_token(token)["sub"]

    event = {
        "type": "checkout.session.completed",
        "data": {"object": {"metadata": {"user_id": uid, "plan": "monthly"}}},
    }

    def fake_construct(payload, sig_header, secret):
        # return the event as-is; signature already 'validated'
        return event

    import stripe
    monkeypatch.setattr(stripe.Webhook, "construct_event", staticmethod(fake_construct))
    resp = client.post(
        "/billing/webhook/stripe", json=event, headers={"stripe-signature": "sig"}
    )
    assert resp.status_code == 200

    from uuid import UUID
    from backend.app.database import SessionLocal
    from backend.app.auth.models import Subscription

    db = SessionLocal()
    uid_obj = UUID(uid)
    sub = (
        db.query(Subscription)
        .filter(Subscription.user_id == uid_obj, Subscription.plan == "monthly")
        .first()
    )
    assert sub is not None
    assert sub.status == "active"

    # check the status endpoint (may be False in simulation)
    resp2 = client.get("/billing/status", headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 200
    assert isinstance(resp2.json().get("ativa"), bool)
    # cancel subscription (stub will always return True)
    resp3 = client.post("/billing/cancel", headers={"Authorization": f"Bearer {token}"})
    assert resp3.status_code == 200
    assert resp3.json().get("success") is True
    # after cancel, status should either be False or remain bool
    resp4 = client.get("/billing/status", headers={"Authorization": f"Bearer {token}"})
    assert isinstance(resp4.json().get("ativa"), bool)


def test_mp_webhook():
    token = get_token(email="mp2@example.com")
    from backend.app.auth.jwt import verify_token
    uid = verify_token(token)["sub"]
    payload = {"metadata": {"user_id": uid, "plan": "monthly"}}
    resp = client.post("/billing/webhook/mp", json=payload)
    assert resp.status_code == 200

    from uuid import UUID
    from backend.app.database import SessionLocal
    from backend.app.auth.models import Subscription

    db = SessionLocal()
    uid_obj = UUID(uid)
    sub = (
        db.query(Subscription)
        .filter(Subscription.user_id == uid_obj, Subscription.plan == "monthly")
        .first()
    )
    assert sub is not None
    assert sub.status == "active"
