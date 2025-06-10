# config.py

# Binance config
# BINANCE_API_KEY = "4ZzQ2hldxBxCg82VCKtdYqIMObVi44159qicFdJECGMxiZbwnYKlVrg8hP4Lepo6"
# BINANCE_API_SECRET = "e1aa34tR0Tvh4QUoXcm5Lsd5wyLTQuDxuz2YK1kYQQeJzP5rttej17CfdnQYlMt1"
# BINANCE_BASE_URL = "https://api.binance.com"

# Binance testnet config
BINANCE_API_KEY = "1d582e6e2c83d92f3da83c375686319647cd0efd1092ad10ef9fbfd7f34e1a8c"
BINANCE_API_SECRET = "7afd9a79a48db4933b8b7e98e6f092de403182fcb465ec5c14e27b6b306a8511"
BINANCE_BASE_URL = "https://testnet.binancefuture.com"

# Trading parameters

# ✅ Symbol mappings and leverage overrides
SYMBOL_CONFIG = {
    "ETH": {"binance": "ETHUSDT", "leverage": 5},
    "BTC": {"binance": "BTCUSDT", "leverage": 5},
    "FARTCOIN": {"binance": "FARTCOINUSDT", "leverage": 5},
    "SOL": {"binance": "SOLUSDT", "leverage": 5},
    "SUI": {"binance": "SUIUSDT", "leverage": 5},
    "ARB": {"binance": "ARBUSDT", "leverage": 5},
    "LINK": {"binance": "LINKUSDT", "leverage": 5},
    "TRUMP": {"binance": "TRUMPUSDT", "leverage": 5},
    "AAVE": {"binance": "AAVEUSDT", "leverage": 5},
}

LEVERAGE_DEFAULT = 5
SIZE_MULTIPLIER = 1
MAX_DAILY_TRADES = 20
MAX_OPEN_POSITIONS = 5
MAX_EXPOSURE = 5000  # USD
ADDRESS_LIST = [
    "0x4b66f4048a0a90fd5ff44abbe5d68332656b78b8",  # real (best)
    "0x3df1ec642ba4427c81ad717cf14281c8dd4af245",  # real
    # "0x14b25601e369b40f5bcd1de0f9a53174e3c59d34",  # bot/real
    "0xdc8cebdbfa78a946639653055e584722bdb5894b",  # bot (FARTCOIN)
    # "0xca230e816bdb34a46960c2f978a30a563d1ae9e0",  # bot (HYPE)
    # "0x1d52fe9bde2694f6172192381111a91e24304397", # bot (aggressive)
]

# Notification (optional)
TELEGRAM_BOT_TOKEN = "7724151045:AAEqPw-MRjLyUaxnx3MVu8Dxdo0zQmKttPU"
TELEGRAM_CHAT_ID = "946227753"
