from fastapi import APIRouter, Body, Request
from pydantic import BaseModel
from . import stripe as stripe_module
from . import mercadopago as mp_module
from ..auth.jwt import verify_token


class CheckoutBody(BaseModel):
    plan: str

router = APIRouter()


@router.post("/checkout/stripe")
def stripe_checkout(body: CheckoutBody = Body(...), request: Request = None):
    token = (request.headers.get("authorization", "") or "").replace("Bearer ", "").strip()
    payload = verify_token(token) if token else None
    user_id = payload.get("sub") if payload else None
    return {"url": stripe_module.create_stripe_checkout(body.plan, user_id)}


@router.post("/checkout/mp")
def mp_checkout(body: CheckoutBody = Body(...), request: Request = None):
    token = (request.headers.get("authorization", "") or "").replace("Bearer ", "").strip()
    payload = verify_token(token) if token else None
    user_id = payload.get("sub") if payload else None
    return {"url": mp_module.create_mp_payment(body.plan, user_id)}


@router.get("/plans")
def list_plans():
    """Return the available subscription plans (keys match frontend IDs)."""
    # convert to list of dicts for easier JSON handling
    return [{"id": k, **v} for k,v in PLANS.items()]


@router.get("/status")
def subscription_status(request: Request = None):
    """Query the payment engine for the current user's subscription status."""
    token = (request.headers.get("authorization", "") or "").replace("Bearer ", "").strip()
    payload = verify_token(token) if token else None
    user_id = payload.get("sub") if payload else None
    if not user_id:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    # import here to avoid circular
    from payment_engine import PaymentEngine
    # we grab engine from app state? easier: reinstantiate with config from main?
    # but main already has global payment_engine; use it via request.app.state if set
    engine = getattr(request.app.state, "payment_engine", None)
    if engine is None:
        engine = PaymentEngine()
    return engine.status_assinatura(user_id)


@router.post("/cancel")
def cancel_subscription(request: Request = None):
    token = (request.headers.get("authorization", "") or "").replace("Bearer ", "").strip()
    payload = verify_token(token) if token else None
    user_id = payload.get("sub") if payload else None
    if not user_id:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    from payment_engine import PaymentEngine
    engine = getattr(request.app.state, "payment_engine", None)
    if engine is None:
        engine = PaymentEngine()
    success = engine.cancelar_assinatura(user_id)
    return {"success": success}


@router.get("/history")
def payment_history(request: Request = None):
    token = (request.headers.get("authorization", "") or "").replace("Bearer ", "").strip()
    payload = verify_token(token) if token else None
    user_id = payload.get("sub") if payload else None
    if not user_id:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    from payment_engine import PaymentEngine
    engine = getattr(request.app.state, "payment_engine", None)
    if engine is None:
        engine = PaymentEngine()
    return engine.historico_pagamentos(user_id)
