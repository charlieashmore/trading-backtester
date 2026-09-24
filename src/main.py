from src.data.market_data import get_market_data
from src.trading.trading_engine import TradingEngine

def main():
    ticker = 'AAPL'
    start = '2023-01-01'
    end = '2023-02-01'

    data = get_market_data(ticker, start, end)
    print(data)

    engine = TradingEngine(1000)
    engine.buy(10, 50)
    print(engine.balance)
    print(engine.shares)
    engine.sell(15, 20)
    print(engine.balance)
    print(engine.shares)
    print(engine.get_portfolio_value(25))
    print(engine.transactions)


if __name__ == "__main__":
    main()