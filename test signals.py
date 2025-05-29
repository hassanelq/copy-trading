# main.py

import asyncio
from listener import HLListener
from config import ADDRESS_LIST
from schemas import TradeSignal
from translator import translate_signal
from executor import BinanceExecutor
from risk import RiskManager
from utils import setup_logger
from notifier import Notifier

# from db import DBHandler

logger = setup_logger("main")

# Initialize system components
executor = BinanceExecutor()
risk_mgr = RiskManager(max_daily_trades=5, max_open_positions=3, max_exposure=1000)
notifier = Notifier()
# db = DBHandler()


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

        # db.record_trade(
        #     symbol=trade["symbol"],
        #     side=trade["side"],
        #     qty=trade["qty"],
        #     price=signal.price,
        #     source_address=signal.address,
        # )

        msg = f"✅ Trade Executed:\n*{trade['side']} {trade['qty']} {trade['symbol']}*"
        logger.info(msg)
        notifier.send(msg)

    except Exception as e:
        err_msg = f"❗ Error: {e}"
        logger.error(err_msg)
        notifier.send(err_msg)


async def test_multiple_trades():
    """Simulate multiple trades to test all components"""
    test_signals = [
        TradeSignal("ETH", "BUY", 0.01, 3500.0, None, "0xtest1"),
        TradeSignal("BTC", "BUY", 0.001, 60000.0, None, "0xtest2"),
        TradeSignal("SOL", "BUY", 0.5, 150.0, None, "0xtest3"),
        TradeSignal("ETH", "SELL", 0.005, 3550.0, None, "0xtest1"),
        TradeSignal("LINK", "BUY", 2, 16.5, None, "0xtest4"),  # may be blocked
        TradeSignal("ARB", "BUY", 10, 1.2, None, "0xtest5"),  # may be blocked
    ]

    for signal in test_signals:
        await process_trade(signal)
        await asyncio.sleep(2)  # Slight delay for clarity/log spacing


if __name__ == "__main__":
    try:
        asyncio.run(test_multiple_trades())
    except KeyboardInterrupt:
        print("\n🔌 Bot stopped by user.")
