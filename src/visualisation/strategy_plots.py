import matplotlib.pyplot as plt
import pandas as pd

def plot_strategy_signals(strategy_name: str, signal_data: pd.DataFrame):
    """
    Plots the signals of a specific trading strategy based on the provided signal data.

    Args:
        strategy_name (str): The name of the trading strategy.
        signal_data (pd.DataFrame): A DataFrame containing the signal data.

    Raises:
        ValueError: If the signal data is empty or does not contain the required columns.
    """

    if signal_data.empty:
        raise ValueError("Signal data is empty. Cannot plot strategy signals.")

    if not all(col in signal_data.columns for col in ['Close', 'Short_MA', 'Long_MA', 'Signal']):
        raise ValueError("Signal data must contain 'Close', 'Short_MA', 'Long_MA', and 'Signal' columns.")

    plt.figure()
    plt.plot(signal_data.index, signal_data['Close'], label='Closing Price', color='blue')
    plt.plot(signal_data.index, signal_data['Short_MA'], label='Short MA', color='red')
    plt.plot(signal_data.index, signal_data['Long_MA'], label='Long MA', color='green')

    buy_rows = signal_data[signal_data['Signal'] == 1]
    sell_rows = signal_data[signal_data['Signal'] == -1]

    plt.scatter(buy_rows.index, buy_rows['Close'], marker='^', color='green', label='Buy')
    plt.scatter(sell_rows.index, sell_rows['Close'], marker='v', color='red', label='Sell')

    plt.title(f'{strategy_name} Strategy Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()

def plot_portfolio_values(portfolio_data: pd.DataFrame, buy_and_hold_data: pd.DataFrame):
    """
    Plots the portfolio value over time for both the strategy and the buy-and-hold approach.

    Args:
        portfolio_data (pd.DataFrame): A DataFrame containing the portfolio value over time for the strategy.
        buy_and_hold_data (pd.DataFrame): A DataFrame containing the portfolio value over time for the buy-and-hold approach.

    Raises:
        ValueError: If either the portfolio data or buy-and-hold data is empty, or if either do not have the required columns.
    """
    if portfolio_data.empty:
        raise ValueError("Portfolio data is empty. Cannot plot portfolio value.")
    if buy_and_hold_data.empty:
        raise ValueError("Buy-and-hold data is empty. Cannot plot buy-and-hold portfolio value.")
    required_columns = ['Date', 'Portfolio Value']
    if not all(col in portfolio_data.columns for col in required_columns):
        raise ValueError("Portfolio data must contain 'Date' and 'Portfolio Value' columns.")
    if not all(col in buy_and_hold_data.columns for col in required_columns):
        raise ValueError("Buy-and-hold data must contain 'Date' and 'Portfolio Value' columns.")

    plt.figure()
    plt.plot(portfolio_data['Date'], portfolio_data['Portfolio Value'], label='Strategy', color='blue')
    plt.plot(buy_and_hold_data['Date'], buy_and_hold_data['Portfolio Value'], label='Buy-and-Hold', color='red')

    plt.title('Portfolio Value Over Time')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.legend()
    plt.tight_layout()