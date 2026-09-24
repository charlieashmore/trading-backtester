from src.data.market_data import get_market_data
from src.strategy.moving_average import calculate_moving_averages, generate_signals
from src.trading.trading_engine import TradingEngine

def main():
    ticker = 'AAPL'
    start = '2023-01-01'
    end = '2024-01-01'

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

    short_window = 20
    long_window = 50
    ma_data = calculate_moving_averages(data, short_window, long_window)
    signals = generate_signals(ma_data)
    print(signals[signals['Signal'] != 0][['Close', 'Short_MA', 'Long_MA', 'Signal']])

if __name__ == "__main__":
    main()