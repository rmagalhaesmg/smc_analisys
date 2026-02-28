from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from ..auth.jwt import verify_token
from ..database import SessionLocal
from ..auth.models import Subscription, User
import uuid


class SubscriptionGuard(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # allow unauthenticated or public endpoints through
        if request.url.path.startswith("/auth") or request.url.path in ["/health", "/docs", "/redoc"]:
            return await call_next(request)
        # allow root and metrics for health checks/tests
        if request.url.path in ["/", "/metrics"]:
            return await call_next(request)

        # allow checkout endpoints (user may not have a subscription yet)
        if request.url.path.startswith("/billing/checkout"):
            return await call_next(request)
        # allow free endpoints for analysis or notifications
        if request.url.path.startswith("/analyze") or request.url.path.startswith("/notifications"):
            return await call_next(request)
        # webhooks are triggered by external services, no token
        if request.url.path.startswith("/billing/webhook"):
            return await call_next(request)

        # require token and valid user
        auth_header = request.headers.get("authorization", "")
        token = auth_header.replace("Bearer ", "").strip()
        if not token:
            raise HTTPException(status_code=401, detail="Token não fornecido")

        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")

        db = SessionLocal()
        try:
            # payload.sub is stored as string in the token; convert to UUID for querying
            try:
                user_id = uuid.UUID(payload.get("sub"))
            except Exception:
                raise HTTPException(status_code=401, detail="Usuário inválido")

            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=401, detail="Usuário não encontrado")
            sub = db.query(Subscription).filter(Subscription.user_id == user.id).first()
            if not sub or sub.status != "active":
                raise HTTPException(status_code=403, detail="Assinatura necessária")
        finally:
            db.close()

        return await call_next(request)
