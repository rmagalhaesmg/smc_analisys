from sqlalchemy import Column, Float, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base
import uuid
from datetime import datetime


class Signal(Base):
    __tablename__ = "signals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    direction = Column(String)  # buy | sell
    entry_price = Column(Float)
    exit_price = Column(Float, nullable=True)
    points = Column(Float, nullable=True)
    success = Column(Boolean, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
