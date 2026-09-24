from src.data.market_data import get_market_data
from src.strategy.moving_average import calculate_moving_averages, generate_signals
from src.backtesting.backtester import run_backtest, calculate_return, calculate_buy_and_hold_return

def main():
    ticker = 'AAPL'
    start = '2023-01-01'
    end = '2024-01-01'

    data = get_market_data(ticker, start, end)
    short_window = 20
    long_window = 50
    ma_data = calculate_moving_averages(data, short_window, long_window)
    signals = generate_signals(ma_data)
    # print(signals[signals['Signal'] != 0][['Close', 'Short_MA', 'Long_MA', 'Signal']])

    portfolio = run_backtest(signals, 10000)
    print(portfolio)

    print(f'Buy and Hold RoR: {calculate_buy_and_hold_return(signals, 10000)}%')
    print(f'Strategy RoR: {calculate_return(portfolio["Portfolio Value"].iloc[0], portfolio["Portfolio Value"].iloc[-1])}%')


if __name__ == "__main__":
    main()