import sys, os
# ensure backend directory is on path so imports of 'app' work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from passlib.context import CryptContext
# override the module-level password context to avoid bcrypt backend issues in tests
import backend.app.auth.router as auth_module
auth_module.pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
# also patch the alternative import path that main uses ('app' vs 'backend.app')
import app.auth.router as auth_module2
auth_module2.pwd_context = auth_module.pwd_context

from fastapi.testclient import TestClient
from backend.main import app
from backend.app.database import Base, engine, SessionLocal
from backend.app.auth.models import User

client = TestClient(app)


def setup_module(module):
    # recreate tables to start fresh
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    Base.metadata.drop_all(bind=engine)


def test_register_and_login():
    # register new user
    resp = client.post("/auth/register", json={"email": "foo@example.com", "password": "secret"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "foo@example.com"

    # duplicate registration should fail
    resp = client.post("/auth/register", json={"email": "foo@example.com", "password": "secret"})
    assert resp.status_code == 400

    # login with wrong password
    resp = client.post("/auth/login", json={"email": "foo@example.com", "password": "wrong"})
    assert resp.status_code == 401

    # login with correct credentials returns token
    resp = client.post("/auth/login", json={"email": "foo@example.com", "password": "secret"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
