# schemas.py
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TradeSignal:
    coin: str
    side: str  # "BUY" or "SELL"
    qty: float
    price: float
    ts: datetime
    address: str
