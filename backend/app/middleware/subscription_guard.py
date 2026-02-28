from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.auth.models import Subscription

class SubscriptionGuard(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # allow auth routes through
        if request.url.path.startswith("/auth"):
            return await call_next(request)

        # require token and valid user
        auth_header = request.headers.get("authorization", "")
        user = get_current_user(authorization=auth_header)
        # check subscription in db
        db = next(get_db())
        sub = db.query(Subscription).filter(Subscription.user_id == user.id).first()
        if not sub or sub.status != "active":
            raise HTTPException(status_code=403, detail="Assinatura necessária")
        return await call_next(request)
