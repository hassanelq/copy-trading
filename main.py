# main.py

import asyncio
from listener import HLListener
from config import ADDRESS_LIST, MAX_DAILY_TRADES, MAX_OPEN_POSITIONS, MAX_EXPOSURE
from schemas import TradeSignal
from translator import translate_signal
from executor import BinanceExecutor
from risk import RiskManager
from utils import setup_logger
from notifier import Notifier

from db import DBHandler

logger = setup_logger("main")

# Initialize system components
executor = BinanceExecutor()
risk_mgr = RiskManager(
    max_daily_trades=MAX_DAILY_TRADES,
    max_open_positions=MAX_OPEN_POSITIONS,
    max_exposure=MAX_EXPOSURE,
)
notifier = Notifier()
db = DBHandler()


async def process_trade(signal: TradeSignal):
    try:
        logger.info(f"📥 Incoming signal: {signal}")

        if not risk_mgr.pre_trade_checks(signal):
            msg = f"⚠️ Trade blocked by risk rules:\n{signal}"
            logger.warning(msg)
            notifier.send(msg)
            return

        trade = translate_signal(signal)

        executor.set_leverage(trade["symbol"], trade["leverage"])
        executor.market_order(trade["symbol"], trade["side"], trade["qty"])
        risk_mgr.update_exposure(signal)

        db.record_trade(
            symbol=trade["symbol"],
            side=trade["side"],
            qty=trade["qty"],
            price=signal.price,
            source_address=signal.address,
        )

        msg = f"✅ Trade Executed:\n*{trade['side']} {trade['qty']} {trade['symbol']}*"
        logger.info(msg)
        notifier.send(msg)

    except ValueError as ve:
        warn_msg = f"⚠️ Trade skipped: {ve}"
        logger.warning(warn_msg)
        notifier.send(warn_msg)
    except Exception as e:
        err_msg = f"❗ Error: {e}"
        logger.error(err_msg)
        notifier.send(err_msg)


async def main():
    listener = HLListener(ADDRESS_LIST)
    await listener.listen(process_trade)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🔌 Bot stopped by user.")
