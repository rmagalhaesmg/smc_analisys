from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from uuid import uuid4
from app.auth.dependencies import get_db
from app.auth.jwt import create_access_token
from app.auth.models import User

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
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    user = User(
        email=body.email,
        password_hash=pwd_context.hash(body.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"email": user.email}


@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not pwd_context.verify(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")
    access = create_access_token({"sub": str(user.id)})
    return {"access_token": access, "token_type": "bearer"}
