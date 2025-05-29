# risk.py

from datetime import datetime, date
from schemas import TradeSignal
from config import MAX_DAILY_TRADES, MAX_OPEN_POSITIONS, MAX_EXPOSURE


class RiskManager:
    def __init__(
        self,
        max_daily_trades=MAX_DAILY_TRADES,
        max_open_positions=MAX_OPEN_POSITIONS,
        max_exposure=MAX_EXPOSURE,
    ):
        self.max_daily_trades = max_daily_trades
        self.max_open_positions = max_open_positions
        self.max_exposure = max_exposure

        self.daily_trade_count = 0
        self.today = date.today()
        self.open_positions = {}  # symbol -> exposure USD

    def reset_if_new_day(self):
        if date.today() != self.today:
            self.today = date.today()
            self.daily_trade_count = 0
            self.open_positions = {}

    def pre_trade_checks(self, signal: TradeSignal) -> bool:
        self.reset_if_new_day()

        symbol = signal.coin.upper()
        usd_value = signal.qty * signal.price

        # Check trade count
        if self.daily_trade_count >= self.max_daily_trades:
            print(f"❌ Rejected: Max daily trades reached ({self.max_daily_trades})")
            return False

        # Check open positions
        if signal.side == "BUY":
            if (
                len(self.open_positions) >= self.max_open_positions
                and symbol not in self.open_positions
            ):
                print(
                    f"❌ Rejected: Max open positions reached ({self.max_open_positions})"
                )
                return False

        # Check exposure
        total_exposure = sum(self.open_positions.values())
        if (total_exposure + usd_value) > self.max_exposure:
            print(f"❌ Rejected: Max exposure exceeded (Limit: ${self.max_exposure})")
            return False

        return True

    def update_exposure(self, signal: TradeSignal):
        symbol = signal.coin.upper()
        usd_value = signal.qty * signal.price

        # Track trade
        self.daily_trade_count += 1

        # Track position
        if signal.side == "BUY":
            self.open_positions[symbol] = self.open_positions.get(symbol, 0) + usd_value
        elif signal.side == "SELL":
            self.open_positions[symbol] = max(
                0, self.open_positions.get(symbol, 0) - usd_value
            )
            if self.open_positions[symbol] == 0:
                del self.open_positions[symbol]
