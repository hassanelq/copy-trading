# schemas.py
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TradeSignal:
    coin: str  # Coin symbol (e.g., "ETH", "BTC")
    side: str  # "BUY" or "SELL"
    qty: float  # Quantity in base units (e.g., ETH, BTC)
    price: float  # Execution price in USDT
    ts: datetime  # Execution timestamp
    address: str  # User address (e.g., "0x1234...abcd")
