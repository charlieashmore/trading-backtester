from src.trading.trading_engine import TradingEngine
import pytest

def test_initialization():
    engine = TradingEngine(1000)
    assert engine.balance == 1000
    assert engine.shares == 0
    assert engine.transactions == []

def test_initialization_negative_balance():
    with pytest.raises(ValueError, match="Balance cannot be negative."):
        TradingEngine(-100)

def test_buy_shares():
    engine = TradingEngine(1000)
    engine.buy(10, 50)
    assert engine.balance == 500
    assert engine.shares == 50
    assert engine.transactions[-1] == {'type': 'buy', 'price': 10, 'shares': 50}

@pytest.mark.parametrize("price, shares", [
    (10, -5),
    (10, 0),
    (10, 4.5),
    (-10, 5),
    (0, 5)
])
def test_buy_shares_invalid_parameters(price, shares):
    engine = TradingEngine(1000)
    with pytest.raises(ValueError):
        engine.buy(price, shares)

    assert engine.balance == 1000
    assert engine.shares == 0
    assert engine.transactions == []

def test_buy_shares_insufficient_balance():
    engine = TradingEngine(100)
    with pytest.raises(ValueError, match="Insufficient balance to complete the purchase."):
        engine.buy(10, 20)

    assert engine.balance == 100
    assert engine.shares == 0
    assert engine.transactions == []

def test_sell_shares():
    engine = TradingEngine(1000)
    engine.buy(10, 50)
    engine.sell(15, 20)
    assert engine.balance == 800
    assert engine.shares == 30
    assert engine.transactions[-1] == {'type': 'sell', 'price': 15, 'shares': 20}

@pytest.mark.parametrize("price, shares", [
    (10, -5),
    (10, 0),
    (10, 4.5),
    (-10, 5),
    (0, 5)
])
def test_sell_shares_invalid_parameters(price, shares):
    engine = TradingEngine(1000)
    engine.buy(10, 50)
    with pytest.raises(ValueError):
        engine.sell(price, shares)

    assert engine.balance == 500
    assert engine.shares == 50
    assert engine.transactions == [{'type': 'buy', 'price': 10, 'shares': 50}]

def test_sell_shares_insufficient_shares():
    engine = TradingEngine(1000)
    engine.buy(10, 50)
    with pytest.raises(ValueError, match="Insufficient shares to complete the sale."):
        engine.sell(10, 60)

    assert engine.balance == 500
    assert engine.shares == 50
    assert engine.transactions == [{'type': 'buy', 'price': 10, 'shares': 50}]

def test_get_portfolio_value():
    engine = TradingEngine(1000)
    engine.buy(10, 50)
    portfolio_value = engine.get_portfolio_value(15)
    assert portfolio_value == 1250

def test_negative_portfolio_value():
    engine = TradingEngine(1000)
    engine.buy(10, 50)
    with pytest.raises(ValueError, match="Current price cannot be negative."):
        engine.get_portfolio_value(-10)