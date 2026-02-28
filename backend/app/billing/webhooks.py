from fastapi import APIRouter, Request
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.models import Subscription
from app.billing.plans import PLANS

router = APIRouter()


@router.post("/stripe")
async def stripe_webhook(request: Request, db: Session = next(get_db())):
    payload = await request.json()
    metadata = payload.get("data", {}).get("object", {}).get("metadata", {})

    user_id = metadata.get("user_id")
    plan_key = metadata.get("plan")

    if not user_id or not plan_key:
        return {"status": "ignored"}

    plan = PLANS[plan_key]

    sub = Subscription(
        user_id=user_id,
        plan=plan_key,
        status="active",
        expires_at=datetime.utcnow() + timedelta(days=plan["duration_days"])
    )
    db.add(sub)
    db.commit()

    return {"status": "ok"}


@router.post("/mp")
async def mercadopago_webhook(request: Request, db: Session = next(get_db())):
    payload = await request.json()
    metadata = payload.get("metadata", {})

    user_id = metadata.get("user_id")
    plan_key = metadata.get("plan")

    if not user_id or not plan_key:
        return {"status": "ignored"}

    plan = PLANS[plan_key]

    sub = Subscription(
        user_id=user_id,
        plan=plan_key,
        status="active",
        expires_at=datetime.utcnow() + timedelta(days=plan["duration_days"])
    )
    db.add(sub)
    db.commit()

    return {"status": "ok"}
