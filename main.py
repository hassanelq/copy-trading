# main.py

import asyncio
from listener import HLListener
from config import ADDRESS_LIST
from schemas import TradeSignal


async def process_trade(signal: TradeSignal):
    print("✅ TradeSignal received:")
    print(
        f"{signal.coin} | {signal.side} | Qty: {signal.qty} @ {signal.price} | {signal.ts} | {signal.address}"
    )


if __name__ == "__main__":
    listener = HLListener(ADDRESS_LIST)
    asyncio.run(listener.listen(process_trade))
