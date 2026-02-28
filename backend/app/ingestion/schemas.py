from pydantic import BaseModel
from datetime import datetime


class ProfitCSVRow(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    delta: float
    trades: int
