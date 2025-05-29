# run_db.py
from db import DBHandler

handler = DBHandler()  # This uses "sqlite:///copytrader.db"

handler.record_trade(
    symbol="BTCUSDT",
    side="BUY",
    qty=0.5,
    price=30000.0,
    source_address="0xabc123"
)

print("Trade recorded.")
