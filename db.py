# db.py

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

Base = declarative_base()


# ---- Trade Table ----
class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    side = Column(String)
    qty = Column(Float)
    price = Column(Float)
    usd_value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_address = Column(String)


# ---- DB Handler ----
class DBHandler:
    def __init__(self, db_path="sqlite:///copytrader.db"):
        self.engine = create_engine(db_path, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def record_trade(self, symbol, side, qty, price, source_address):
        usd_value = qty * price
        session = self.Session()
        trade = Trade(
            symbol=symbol,
            side=side,
            qty=qty,
            price=price,
            usd_value=usd_value,
            source_address=source_address,
        )
        session.add(trade)
        session.commit()
        session.close()

    def get_all_trades(self):
        session = self.Session()
        trades = session.query(Trade).all()
        session.close()
        return trades
