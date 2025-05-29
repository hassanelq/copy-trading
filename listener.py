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
        self.initial_connection_done = False

    async def listen(self, callback: Callable[[TradeSignal], None]):
        while True:
            try:
                async with websockets.connect(HL_WS_URL) as ws:
                    self.ws = ws
                    if not self.initial_connection_done:
                        logger.info("✅ Connected to Hyperliquid WebSocket")
                        self.initial_connection_done = True

                    for addr in self.addresses:
                        await self.subscribe_user_fills(addr)

                    async for message in ws:
                        await self.handle_message(message, callback)

            except Exception as e:
                logger.error(f"❌ WebSocket error: {e}")
                logger.warning("🔄 Attempting reconnect in 5 seconds...")
                await asyncio.sleep(5)

    async def subscribe_user_fills(self, address: str):
        sub_msg = {
            "method": "subscribe",
            "subscription": {"type": "userFills", "user": address},
        }
        await self.ws.send(json.dumps(sub_msg))
        if not self.initial_connection_done:
            logger.info(f"🛰️ Subscribed to userFills for {address}")

    async def handle_message(
        self, raw_msg: str, callback: Callable[[TradeSignal], None]
    ):
        msg = json.loads(raw_msg)

        if msg.get("channel") != "userFills":
            return

        fills = msg.get("data", {}).get("fills", [])
        user = msg.get("data", {}).get("user")

        for fill in fills:
            try:
                symbol = fill.get("coin")
                px = fill.get("px")
                sz = fill.get("sz")
                side_raw = fill.get("side")
                time_ms = fill.get("time")

                if None in [symbol, px, sz, side_raw, time_ms]:
                    raise ValueError("Missing required fields")

                # Convert price and size
                price = float(px)
                qty = float(sz)
                ts = datetime.fromtimestamp(time_ms / 1000)

                # Determine side (handle both 'B'/'S' and fallback)
                side = (
                    "BUY"
                    if side_raw == "B"
                    else (
                        "SELL"
                        if side_raw == "S"
                        else ("BUY" if fill.get("isTaker") else "SELL")
                    )
                )

                signal = TradeSignal(
                    coin=symbol,
                    side=side,
                    qty=qty,
                    price=price,
                    ts=ts,
                    address=user,
                )

                logger.info(f"📥 TradeSignal received: {signal}")
                await callback(signal)

            except Exception as e:
                logger.warning(f"⚠️ Skipping malformed fill: {fill} — {e}")
