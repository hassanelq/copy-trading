# listener.py

import asyncio
import json
import websockets
from typing import Callable
from datetime import datetime
from schemas import TradeSignal
from config import ADDRESS_LIST
from utils import setup_logger

logger = setup_logger("listener")

HL_WS_URL = "wss://api.hyperliquid.xyz/ws"


class HLListener:
    def __init__(self, addresses: list[str]):
        self.addresses = addresses
        self.ws = None

    async def listen(self, callback: Callable[[TradeSignal], None]):
        while True:
            try:
                async with websockets.connect(HL_WS_URL) as ws:
                    self.ws = ws
                    logger.info("Connected to Hyperliquid WebSocket")

                    # Subscribe to userFills for each address
                    for addr in self.addresses:
                        await self.subscribe_user_fills(addr)

                    async for message in ws:
                        await self.handle_message(message, callback)

            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                logger.info("Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

    async def subscribe_user_fills(self, address: str):
        sub_msg = {
            "method": "subscribe",
            "subscription": {"type": "userFills", "user": address},
        }
        await self.ws.send(json.dumps(sub_msg))
        logger.info(f"Subscribed to userFills for {address}")

    async def handle_message(
        self, raw_msg: str, callback: Callable[[TradeSignal], None]
    ):
        msg = json.loads(raw_msg)

        if msg.get("channel") != "userFills":
            return

        fills = msg.get("data", {}).get("fills", [])
        user = msg.get("data", {}).get("user")
        for fill in fills:
            symbol = fill.get("coin")
            side = "BUY" if fill.get("isTaker") else "SELL"
            qty = float(fill.get("base"))
            price = float(fill.get("px"))
            ts = datetime.fromtimestamp(fill.get("time") / 1000)

            signal = TradeSignal(
                coin=symbol, side=side, qty=qty, price=price, ts=ts, address=user
            )

            logger.info(f"📥 TradeSignal received: {signal}")
            await callback(signal)
