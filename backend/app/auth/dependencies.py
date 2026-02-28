from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..database import get_db
from .jwt import verify_token
from .models import User
import uuid


def get_current_user(
    authorization: str = Header(default=""),
    db: Session = Depends(get_db),
):
    token = authorization.replace("Bearer ", "").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    # token `sub` is stored as string; convert to UUID for DB queries
    try:
        user_id = uuid.UUID(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Usuário inválido")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return user


def get_user_with_subscription(user=Depends(get_current_user), db: Session = Depends(get_db)):
    # pode implementar verificação de assinatura aqui (ver subscription)
    return user
