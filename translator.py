from config import SIZE_MULTIPLIER, LEVERAGE_DEFAULT, SYMBOL_CONFIG
from typing import Optional
from schemas import TradeSignal


def map_symbol(hl_symbol: str) -> Optional[str]:
    """Map Hyperliquid coin to Binance pair"""
    config = SYMBOL_CONFIG.get(hl_symbol.upper())
    return config["binance"] if config else None


def get_leverage(symbol: str) -> int:
    """Get per-symbol leverage or fallback to default"""
    config = SYMBOL_CONFIG.get(symbol.upper())
    return config.get("leverage", LEVERAGE_DEFAULT) if config else LEVERAGE_DEFAULT


def calc_order_qty(price: float, usd_size: float) -> float:
    """Calculate Binance quantity from USD size"""
    return round(usd_size / price, 3)


def translate_signal(signal: TradeSignal) -> dict:
    """Convert TradeSignal to Binance-ready order dict"""
    binance_symbol = map_symbol(signal.coin)
    if not binance_symbol:
        raise ValueError(f"Unsupported coin: {signal.coin}")

    usd_size = signal.qty * signal.price * SIZE_MULTIPLIER
    qty = calc_order_qty(signal.price, usd_size)
    leverage = get_leverage(signal.coin)

    return {
        "symbol": binance_symbol,
        "side": signal.side,
        "qty": qty,
        "leverage": leverage,
    }
