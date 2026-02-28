import stripe
import os
from app.billing.plans import PLANS

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")


def create_stripe_checkout(plan_key: str, user_id: str):
    plan = PLANS[plan_key]

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "brl",
                "product_data": {"name": f"SMC {plan_key}"},
                "unit_amount": int(plan["price"] * 100),
            },
            "quantity": 1
        }],
        success_url=os.getenv("FRONTEND_URL", "http://localhost:3000") + "/success",
        cancel_url=os.getenv("FRONTEND_URL", "http://localhost:3000") + "/cancel",
        metadata={
            "user_id": user_id,
            "plan": plan_key
        }
    )
    return session.url
