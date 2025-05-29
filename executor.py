# executor.py

import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL
from utils import setup_logger

logger = setup_logger("executor")


class BinanceExecutor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": BINANCE_API_KEY})

    def _sign_params(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            BINANCE_API_SECRET.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def set_leverage(self, symbol: str, leverage: int):
        """Set leverage for a futures symbol"""
        url = f"{BINANCE_BASE_URL}/fapi/v1/leverage"
        payload = self._sign_params(
            {
                "symbol": symbol,
                "leverage": leverage,
            }
        )

        r = self.session.post(url, params=payload)
        if r.status_code == 200:
            logger.info(f"✅ Leverage set: {symbol} → {leverage}x")
        else:
            logger.error(f"❌ Failed to set leverage: {r.text}")
            raise Exception(f"Binance error: {r.text}")

    def market_order(self, symbol: str, side: str, qty: float):
        """Place a market order on Binance Futures"""
        url = f"{BINANCE_BASE_URL}/fapi/v1/order"
        payload = self._sign_params(
            {"symbol": symbol, "side": side, "type": "MARKET", "quantity": qty}
        )

        r = self.session.post(url, params=payload)
        if r.status_code == 200:
            logger.info(f"✅ Market order placed: {side} {qty} {symbol}")
            return r.json()
        else:
            logger.error(f"❌ Order failed: {r.text}")
            raise Exception(f"Binance error: {r.text}")
