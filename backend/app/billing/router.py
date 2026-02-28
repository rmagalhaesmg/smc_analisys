from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.billing.stripe import create_stripe_checkout
from app.billing.mercadopago import create_mp_payment

router = APIRouter()


@router.post("/checkout/stripe")
def stripe_checkout(plan: str, user=Depends(get_current_user)):
    return {"url": create_stripe_checkout(plan, str(user.id))}


@router.post("/checkout/mp")
def mp_checkout(plan: str, user=Depends(get_current_user)):
    return {"url": create_mp_payment(plan, str(user.id))}
