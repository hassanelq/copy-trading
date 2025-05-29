# translator.py

from config import SIZE_MULTIPLIER, LEVERAGE_DEFAULT
from typing import Optional
from schemas import TradeSignal
import math

# Basic mapping — expand as needed
SYMBOL_MAP = {
    "ETH": "ETHUSDT",
    "BTC": "BTCUSDT",
    "SOL": "SOLUSDT",
    "ARB": "ARBUSDT",
    "LINK": "LINKUSDT",
}


def map_symbol(hl_symbol: str) -> Optional[str]:
    """Map Hyperliquid coin to Binance pair"""
    return SYMBOL_MAP.get(hl_symbol.upper())


def get_leverage(symbol: str, override_map: dict[str, int]) -> int:
    """Use override or default leverage"""
    return override_map.get(symbol.upper(), LEVERAGE_DEFAULT)


def calc_order_qty(price: float, usd_size: float) -> float:
    """
    Calculate Binance order quantity from USD value.
    You can round this based on Binance's lot size filter.
    """
    return round(usd_size / price, 3)


def translate_signal(signal: TradeSignal, override_map: dict[str, int] = {}) -> dict:
    """
    Convert TradeSignal to a Binance-ready trade dict
    """
    binance_symbol = map_symbol(signal.coin)
    if not binance_symbol:
        raise ValueError(f"Unsupported coin: {signal.coin}")

    usd_size = signal.qty * signal.price * SIZE_MULTIPLIER
    qty = calc_order_qty(signal.price, usd_size)
    leverage = get_leverage(signal.coin, override_map)
    side = signal.side  # Already "BUY" or "SELL"

    return {"symbol": binance_symbol, "side": side, "qty": qty, "leverage": leverage}
