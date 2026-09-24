import pandas as pd

def calculate_moving_averages(data : pd.DataFrame, short_window : int, long_window : int):
    """
    Calculate short-term and long-term moving averages for the given data.

    Parameters:
    - data: A pandas DataFrame containing market data with a 'Close' column.
    - short_window: The window size for the short-term moving average.
    - long_window: The window size for the long-term moving average.

    Returns:
    A pandas DataFrame with two new columns: 'Short_MA' and 'Long_MA'.
    """
    if not isinstance(short_window, int) or not isinstance(long_window, int):
        raise ValueError("Window sizes must be integers.")
    if short_window <= 0 or long_window <= 0:
        raise ValueError("Window sizes must be positive integers.")
    if short_window >= long_window:
        raise ValueError("Short window must be less than long window.")

    copy_data = data.copy()
    copy_data['Short_MA'] = copy_data['Close'].rolling(window=short_window).mean()
    copy_data['Long_MA'] = copy_data['Close'].rolling(window=long_window).mean()
    return copy_data

def generate_signals(data : pd.DataFrame) -> pd.DataFrame:
    """
    Generate buy/sell signals based on moving average crossovers.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame containing market data with 'Short_MA' and 'Long_MA' columns (generated from passing market data through the calculate_moving_averages function).

    Returns:
        pd.DataFrame: A pandas DataFrame with a new column 'Signal' indicating buy (1), sell (-1), or hold (0).

    Raises:
        ValueError: If the input DataFrame does not contain the required 'Short_MA' and 'Long_MA' columns.
    """
    if 'Short_MA' not in data.columns or 'Long_MA' not in data.columns:
        raise ValueError("Data must contain 'Short_MA' and 'Long_MA' columns.")

    copy_data = data.copy()
    copy_data['Signal'] = 0
    copy_data.loc[(copy_data['Short_MA'] > copy_data['Long_MA']) & (copy_data['Short_MA'].shift(1) <= copy_data['Long_MA'].shift(1)), 'Signal'] = 1
    copy_data.loc[(copy_data['Short_MA'] < copy_data['Long_MA']) & (copy_data['Short_MA'].shift(1) >= copy_data['Long_MA'].shift(1)), 'Signal'] = -1
    return copy_data
