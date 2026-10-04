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

    plt.show()