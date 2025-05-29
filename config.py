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
    "ETH": {"binance": "ETHUSDT", "leverage": 15},
    "BTC": {"binance": "BTCUSDT", "leverage": 20},
    "SOL": {"binance": "SOLUSDT", "leverage": 10},
    "ARB": {"binance": "ARBUSDT", "leverage": 8},
    "LINK": {"binance": "LINKUSDT", "leverage": 5},
    "FARTCOIN": {"binance": "FARTCOINUSDT", "leverage": 10},
    "TRUMP": {"binance": "TRUMPUSDT", "leverage": 10},
}

LEVERAGE_DEFAULT = 10
SIZE_MULTIPLIER = 1.5
MAX_DAILY_TRADES = 20
MAX_OPEN_POSITIONS = 5
MAX_EXPOSURE = 5000  # USD
ADDRESS_LIST = [
    "0x4b66f4048a0a90fd5ff44abbe5d68332656b78b8",
    "0xca230e816bdb34a46960c2f978a30a563d1ae9e0",
    "0x8ea8b94cbb847095cd1c9599782c6e7b6d9e930d",
    "0xdc685cbb04b04aa262f9e541d9e4d6f0a680a03a",
    "0x1d52fe9bde2694f6172192381111a91e24304397",
    "0x94ab9eb9c49efb110870cfb713933bef4414b60b",
    "0xe9c2df5b14c7f476e8a5895d5b0c6b015e87bf2e",
    "0x8fc7c0442e582bca195978c5a4fdec2e7c5bb0f7",
    "0x9bf759b22E365D8b94a0679faf1010c0C7A78004",
    "0x4f93fead39b70a1824f981a54d4e55b278e9f760",
    "0x9dea4d13ac1c469b7fe9049d43835df1be143ec0",
    "0x420ab45e0bd8863569a5efbb9c05d91f40624641",
    "0xa1cb16d2b17202c336138f765559dfc73830b1fb",
    "0x265bda080f9107223a74455201674538c32482b0",
    "0x360537542135943e8fc1562199aea6d0017f104b",
    "0x1111bbf435a2b5e0f17e97a0764c58f2ed4bf167",
    "0x67b6baae5bd3c1b332b37859d8f12ecf78fd0752",
    "0x41206f8efb51e5039e5b46e04e7866a4849f72d2",
    "0x5a54ad9860b08aaee07174887f9ee5107b0a2e72",
    "0x7625dc67deab1864570ad816f59a9b867f280e49",
    "0x6859da14835424957a1e6b397d8026b1d9ff7e1e",
    "0xb83de012dba672c76a7dbbbf3e459cb59d7d6e36",
    "0xafd9cfc5d4a4af11cc472379f48315ae21e9acd7",
    "0x2e5af7bc3ca942491366ae5672fdc702e9a4fb3e",
    "0x388855cd19e68891bf6eb081e969b7ee9ca1dcdd",
    "0xe25173b3558e8644d719f2cd3095dccbf5efeaba",
    "0xa2ce501d9c0c5e23d34272f84402cfb7835b3126",
    "0x2ba553d9f990a3b66b03b2dc0d030dfc1c061036",
    "0x863b676e5e4fea0541062c32983dc8f84749ca6d",
    "0x64a4fbb71858f681f3fa10a42b34180a9a48088d",
    "0x75161cdd2ee68383d0c90ddbbd46d20b9daa11ab",
    "0x94b5d25964fe7abf11ae5399ae1eb61de7151faf",
    "0xc11c720c554db80a89ffea960633429be61c6a10",
    "0x3e9b6020cb47785b9416e83fad561a72d2af4de8",
    "0x9458f423df6569f053358ee9906613cd69c1ec04",
    "0x844b6ab0079fb36e6a99cba877574acd8f1e7f42",
    "0xeb93e6fc46b78c19bfe3264afabccae410956389",
    "0x1072c71c11c15de15ff664c8736dc9a04966fabd",
    "0xe58fa37043372d7c5123ce74e01ea51db299aca0",
    "0xbfc79c444c41a74516bf31237ebf586a231480b4",
]

# Notification (optional)
TELEGRAM_BOT_TOKEN = "7724151045:AAEqPw-MRjLyUaxnx3MVu8Dxdo0zQmKttPU"
TELEGRAM_CHAT_ID = "946227753"
