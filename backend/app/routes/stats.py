from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth.dependencies import get_current_user
from ..models.signal import Signal
from sqlalchemy import func

router = APIRouter()


@router.get("/signals")
def signal_stats(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    total = db.query(Signal).filter_by(user_id=user.id).count()
    wins = db.query(Signal).filter_by(user_id=user.id, success=True).count()
    avg_points = db.query(func.avg(Signal.points)).filter_by(user_id=user.id).scalar()

    return {
        "total_signals": total,
        "wins": wins,
        "assertiveness": round((wins / total) * 100, 2) if total else 0,
        "avg_points": round(avg_points or 0, 2)
    }
