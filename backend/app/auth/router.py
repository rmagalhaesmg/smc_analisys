from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from uuid import uuid4
import logging

from .dependencies import get_db
from .jwt import create_access_token
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


class RegisterBody(BaseModel):
    email: str
    password: str
    nome: str = ""


class LoginBody(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(body: RegisterBody, db: Session = Depends(get_db)):
    # guard against duplicate
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    user = User(
        email=body.email,
        password_hash=pwd_context.hash(body.password)
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        logging.getLogger("smc.auth").exception("Erro ao registrar usuário")
        # fallback to in-memory engine if available
        # try to fall back to the in‑memory engine defined in main.py
        try:
            from backend import main as _main
            auth_engine = getattr(_main, "auth_engine", None)
            if auth_engine:
                auth_engine.register_user(body.email, body.password, body.email)
                return {"email": body.email, "warning": "registered in memory due to db error"}
        except ImportError:
            logging.getLogger("smc.auth").warning("could not import main.auth_engine for fallback")
        raise HTTPException(status_code=500, detail="falha ao criar usuário")
    return {"email": user.email}


@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if user:
        if not pwd_context.verify(body.password, user.password_hash):
            raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")
        access = create_access_token({"sub": str(user.id)})
        return {"access_token": access, "token_type": "bearer"}
    # if DB lookup failed, try the in‑memory auth engine
    try:
        from backend import main as _main
        auth_engine = getattr(_main, "auth_engine", None)
    except ImportError:
        auth_engine = None
    if auth_engine:
        auth_res = auth_engine.authenticate_user(body.email, body.password)
        if auth_res.get("success"):
            access = create_access_token({"sub": body.email})
            return {"access_token": access, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")
