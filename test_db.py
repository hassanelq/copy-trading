import tempfile
from db import DBHandler

def get_test_db_handler():
    # Use a temporary SQLite database for testing
    db_fd, db_path = tempfile.mkstemp()
    db_url = f"sqlite:///{db_path}"
    handler = DBHandler(db_url)
    return handler

def test_record_and_get_all_trades():
    handler = get_test_db_handler()

    # Record a trade
    handler.record_trade(
        symbol="BTCUSDT",
        side="BUY",
        qty=0.5,
        price=30000.0,
        source_address="0xabc123"
    )

    # Retrieve all trades
    trades = handler.get_all_trades()
    assert len(trades) == 1
    trade = trades[0]
    assert trade.symbol == "BTCUSDT"
    assert trade.side == "BUY"
    assert trade.qty == 0.5
    assert trade.price == 30000.0
    assert trade.usd_value == 15000.0
    assert trade.source_address == "0xabc123"
    assert trade.timestamp is not None
