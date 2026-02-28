from fastapi import APIRouter, Request, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth.models import Subscription
from .plans import PLANS

router = APIRouter()


@router.post("/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    # verify signature
    sig_header = request.headers.get("stripe-signature", "")
    secret = request.app.state.stripe_webhook_secret if hasattr(request.app.state, "stripe_webhook_secret") else None
    body = await request.body()
    if secret:
        import stripe as _stripe
        try:
            _stripe.Webhook.construct_event(payload=body, sig_header=sig_header, secret=secret)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid stripe webhook: {e}")

    payload = await request.json()
    # only act on successful checkout events
    event_type = payload.get("type")
    if event_type not in ("checkout.session.completed", "payment_intent.succeeded"):
        return {"status": "ignored"}

    metadata = payload.get("data", {}).get("object", {}).get("metadata", {})

    user_id = metadata.get("user_id")
    plan_key = metadata.get("plan")

    if not user_id or not plan_key:
        return {"status": "ignored"}

    plan = PLANS.get(plan_key)
    if not plan:
        return {"status": "ignored"}

    # convert user id string to UUID object for queries/insertion
    from uuid import UUID
    try:
        user_uuid = UUID(user_id)
    except Exception:
        return {"status": "ignored"}

    # upsert subscription: extend or create
    existing = db.query(Subscription).filter(Subscription.user_id == user_uuid, Subscription.plan == plan_key).first()
    expires = datetime.utcnow() + timedelta(days=plan["duration_days"])
    if existing:
        existing.status = "active"
        existing.expires_at = expires
    else:
        sub = Subscription(
            user_id=user_uuid,
            plan=plan_key,
            status="active",
            expires_at=expires
        )
        db.add(sub)
    db.commit()

    return {"status": "ok"}


@router.post("/mp")
async def mercadopago_webhook(request: Request, db: Session = Depends(get_db)):
    # MP signature validation would go here in production
    secret = request.app.state.mp_webhook_secret if hasattr(request.app.state, "mp_webhook_secret") else None
    # pretend to validate using header or query param
    if secret:
        sig = request.headers.get("x-mp-signature", "")
        if sig != secret:
            raise HTTPException(status_code=400, detail="Invalid mercadopago webhook")

    payload = await request.json()
    # assume webhook sent after approved payment
    metadata = payload.get("metadata", {})

    user_id = metadata.get("user_id")
    plan_key = metadata.get("plan")

    if not user_id or not plan_key:
        return {"status": "ignored"}

    plan = PLANS.get(plan_key)
    if not plan:
        return {"status": "ignored"}

    from uuid import UUID
    try:
        user_uuid = UUID(user_id)
    except Exception:
        return {"status": "ignored"}

    existing = db.query(Subscription).filter(Subscription.user_id == user_uuid, Subscription.plan == plan_key).first()
    expires = datetime.utcnow() + timedelta(days=plan["duration_days"])
    if existing:
        existing.status = "active"
        existing.expires_at = expires
    else:
        sub = Subscription(
            user_id=user_uuid,
            plan=plan_key,
            status="active",
            expires_at=expires
        )
        db.add(sub)
    db.commit()

    return {"status": "ok"}
