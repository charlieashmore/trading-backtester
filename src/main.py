from src.data.market_data import get_market_data
from src.strategy.moving_average import calculate_moving_averages, generate_signals
from src.backtesting.backtester import run_backtest, calculate_buy_and_hold_values
from src.visualisation.strategy_plots import plot_portfolio_values, plot_strategy_signals
import matplotlib.pyplot as plt

def main():
    ticker = 'AAPL'
    start = '2023-01-01'
    end = '2024-01-01'

    data = get_market_data(ticker, start, end)
    short_window = 20
    long_window = 50
    ma_data = calculate_moving_averages(data, short_window, long_window)
    signals = generate_signals(ma_data)

    strategy_name = "Moving Average Crossover"
    plot_strategy_signals(strategy_name, signals)

    start_balance = 10000
    buy_and_hold_values = calculate_buy_and_hold_values(data, start_balance)
    portfolio = run_backtest(signals, start_balance)
    plot_portfolio_values(portfolio, buy_and_hold_values)

    plt.show()

if __name__ == "__main__":
    main()