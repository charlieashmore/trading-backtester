from src.data.market_data import get_market_data
from src.strategy.moving_average import calculate_moving_averages, generate_signals
from src.backtesting.backtester import run_backtest, calculate_buy_and_hold_values
from src.visualisation.strategy_plots import plot_portfolio_values, plot_strategy_signals
import matplotlib.pyplot as plt

def main():
    strategy_name = "Moving Average Crossover"
    while True:
        try:
            # get inputs
            user_inputs = get_user_input()
            ticker, start_date, end_date, short_window, long_window, starting_balance = user_inputs

            # get data from input
            market_data = get_market_data(ticker, start_date, end_date)
            moving_average_data = calculate_moving_averages(market_data, short_window, long_window)
            signals_data = generate_signals(moving_average_data)

            # run backtest and calculate buy and hold values
            portfolio_values = run_backtest(signals_data, starting_balance)
            buy_and_hold_values = calculate_buy_and_hold_values(market_data, starting_balance)

            break
        except ValueError as e:
            print(f"An error occurred: {e}")
            print("Please try again with valid inputs.\n")

    # plot performance of the strategy and buy and hold
    plot_strategy_signals(strategy_name, signals_data, ticker)
    plot_portfolio_values(portfolio_values, buy_and_hold_values, ticker)
    plt.show()

def get_user_input() -> tuple:
    """
    Get user input for the stock ticker, start date, end date, short trading window, and long trading window, and starting balance.

    Returns:
        user_inputs (tuple): A tuple containing the stock ticker (str), start date (str), end date (str), short trading window (int), long trading window (int), and starting balance (float).
    """
    ticker = input("Enter the stock ticker (e.g., AAPL): ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    short_window = int(input("Enter the short trading window (e.g., 20): "))
    long_window = int(input("Enter the long trading window (e.g., 50): "))
    starting_balance = float(input("Enter the starting balance available for trading: "))
    user_inputs = (ticker, start_date, end_date, short_window, long_window, starting_balance)
    return user_inputs

if __name__ == "__main__":
    main()


