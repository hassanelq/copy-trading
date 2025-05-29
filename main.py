# main.py

import asyncio
from listener import HLListener
from config import ADDRESS_LIST
from schemas import TradeSignal


async def process_trade(signal: TradeSignal):
    print("Processing:", signal)


if __name__ == "__main__":
    listener = HLListener(ADDRESS_LIST)
    asyncio.run(listener.listen(process_trade))
