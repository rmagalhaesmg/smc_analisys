"""
Payment Engine - Stub Implementation
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class PaymentConfig:
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    mp_access_token: str = ""
    mp_notification_url: str = "http://localhost:8000"
    modo_simulacao: bool = True

class PaymentEngine:
    def __init__(self, config: Optional[PaymentConfig] = None):
        self.config = config or PaymentConfig()
        self.transactions = {}  # in-sim transactions for demo

    # -- backward-compatible stubs ------------------------------------------------
    def create_payment_intent(self, amount: float, currency: str = "USD") -> dict:
        """Legacy stub, keeps old endpoints functioning."""
        intent_id = f"pi_{datetime.now().timestamp()}"
        self.transactions[intent_id] = {
            "amount": amount,
            "currency": currency,
            "status": "pending",
            "created_at": datetime.now()
        }
        return {
            "success": True,
            "intent_id": intent_id,
            "amount": amount,
            "currency": currency
        }

    def confirm_payment(self, intent_id: str, payment_method_id: str) -> dict:
        if intent_id not in self.transactions:
            return {"success": False, "error": "Intent not found"}
        self.transactions[intent_id]["status"] = "confirmed"
        self.transactions[intent_id]["payment_method"] = payment_method_id
        return {"success": True, "intent_id": intent_id, "status": "confirmed"}

    def refund_payment(self, intent_id: str) -> dict:
        if intent_id not in self.transactions:
            return {"success": False, "error": "Intent not found"}
        self.transactions[intent_id]["status"] = "refunded"
        return {"success": True, "intent_id": intent_id, "status": "refunded"}

    def get_payment_status(self, intent_id: str) -> dict:
        if intent_id not in self.transactions:
            return {"success": False, "error": "Intent not found"}
        return {"success": True, "intent_id": intent_id, "status": self.transactions[intent_id]["status"]}

    # -- new helpers that wrap the billing package -------------------------------
    async def criar_checkout_stripe(self, user_id: str, email: str, plano: str):
        # forward to the billing helper, record an event if desired
        from app.billing.stripe import create_stripe_checkout
        url = create_stripe_checkout(plano, user_id)
        return {"url": url}

    async def criar_preferencia_mp(self, user_id: str, email: str, plano: str):
        from app.billing.mercadopago import create_mp_payment
        url = create_mp_payment(plano, user_id)
        return {"url": url}

    # -- status & subscription management ---------------------------------------
    def status_assinatura(self, user_id: str) -> dict:
        """Return whether the user has an active subscription.
        Adds `days_remaining` when active.
        """
        if self.config.modo_simulacao:
            return {"ativa": False}
        from backend.app.database import SessionLocal
        from backend.app.auth.models import Subscription
        db = SessionLocal()
        now = datetime.utcnow()
        sub = (
            db.query(Subscription)
            .filter(Subscription.user_id == user_id, Subscription.status == "active")
            .order_by(Subscription.expires_at.desc())
            .first()
        )
        db.close()
        if not sub or sub.expires_at < now:
            return {"ativa": False}
        days = (sub.expires_at - now).days
        return {
            "ativa": True,
            "plan": sub.plan,
            "expires_at": sub.expires_at.isoformat(),
            "days_remaining": days,
        }

    def cancelar_assinatura(self, user_id: str) -> bool:
        if self.config.modo_simulacao:
            return True
        from backend.app.database import SessionLocal
        from backend.app.auth.models import Subscription
        db = SessionLocal()
        updated = False
        for s in db.query(Subscription).filter(Subscription.user_id == user_id, Subscription.status == "active").all():
            s.status = "cancelled"
            updated = True
        db.commit()
        db.close()
        return updated

    def historico_pagamentos(self, user_id: str) -> list:
        """Return subscription records as payment history."""
        if self.config.modo_simulacao:
            return []
        from backend.app.database import SessionLocal
        from backend.app.auth.models import Subscription
        db = SessionLocal()
        subs = db.query(Subscription).filter(Subscription.user_id == user_id).order_by(Subscription.expires_at.desc()).all()
        result = [{
            "plan": s.plan,
            "status": s.status,
            "expires_at": s.expires_at.isoformat() if s.expires_at else None
        } for s in subs]
        db.close()
        return result
