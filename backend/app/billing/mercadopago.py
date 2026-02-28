import mercadopago
import os
from app.billing.plans import PLANS

sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN", ""))


def create_mp_payment(plan_key: str, user_id: str):
    plan = PLANS[plan_key]

    preference = {
        "items": [{
            "title": f"SMC {plan_key}",
            "quantity": 1,
            "currency_id": "BRL",
            "unit_price": plan["price"]
        }],
        "metadata": {
            "user_id": user_id,
            "plan": plan_key
        },
        "notification_url": os.getenv("BACKEND_URL", "http://localhost:8000") + "/billing/webhook/mp"
    }

    response = sdk.preference().create(preference)
    return response["response"]["init_point"]
