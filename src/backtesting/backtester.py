import pandas as pd
from src.trading.trading_engine import TradingEngine

def run_backtest(signals_data: pd.DataFrame, start_balance: float) -> pd.DataFrame:
    """
    Run a backtest using the provided signals data and starting balance (trading is completed on the following days open price after the signal is generated).

    Parameters:
        signals_data (pd.DataFrame): A pandas DataFrame containing market data with 'Signal' column (generated from passing market data through the generate_signals function).
        start_balance (float): The initial amount of money available for trading.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the portfolio value over time, along with the balance and number of shares held.

    Raises:
        ValueError: If signals_data does not contain the required 'Signal', 'Close', and 'Open' columns.
    """
    if 'Signal' not in signals_data.columns:
        raise ValueError("signals_data must contain a 'Signal' column")
    if 'Close' not in signals_data.columns:
        raise ValueError("signals_data must contain a 'Close' column")
    if 'Open' not in signals_data.columns:
        raise ValueError("signals_data must contain a 'Open' column")

    portfolio_history = []
    engine = TradingEngine(start_balance)
    signal_data_copy = signals_data.copy()
    signal_data_copy['Signal'] = signal_data_copy['Signal'].shift(1).fillna(0)
    for index, row in signal_data_copy.iterrows():
        trading_price = row['Open']
        closing_price = row['Close']
        if row['Signal'] == 1:
            shares_to_buy = int(engine.balance // trading_price)
            if shares_to_buy > 0:
                engine.buy(trading_price, shares_to_buy)
        elif row['Signal'] == -1:
            shares_to_sell = engine.shares
            if shares_to_sell > 0:
                engine.sell(trading_price, shares_to_sell)
        portfolio_value = engine.get_portfolio_value(closing_price)
        portfolio_history.append({
            'Date': index,
            'Portfolio Value': portfolio_value,
            'Balance': engine.balance,
            'Shares': engine.shares,
        })

    portfolio = pd.DataFrame(portfolio_history)
    return portfolio

def calculate_return(start_value: float, end_value: float) -> float:
    """
    Calculate the percentage return between two values.

    Args:
        start_value (float): The initial value.
        end_value (float): The final value.

    Returns:
        float: The percentage return, rounded to two decimal places.

    Raises:
        ValueError: If the start_value is zero (to avoid division by zero).
    """
    if start_value == 0:
        raise ValueError("Start value cannot be zero for return calculation.")
    return round(((end_value - start_value) / start_value) * 100, 2)

def calculate_buy_and_hold_return(signals_data: pd.DataFrame, start_balance: float) -> float:
    """
    Calculate the buy-and-hold return based on the provided market data.

    Args:
        signals_data (pd.DataFrame): A DataFrame containing market data with a 'Close' column.
        start_balance (float): The initial amount of money available for trading.

    Returns:
        float: The buy-and-hold return as a percentage, rounded to two decimal places.

    Raises:
        ValueError: If the signals_data does not contain a 'Close' column or if the start_balance is zero or negative.
    """
    if signals_data.empty:
        raise ValueError("signals_data is empty. Cannot calculate buy-and-hold return.")
    if 'Close' not in signals_data.columns:
        raise ValueError("signals_data must contain a 'Close' column")
    if start_balance == 0:
        raise ValueError("Starting balance cannot be zero.")
    if start_balance < 0:
        raise ValueError("Starting balance cannot be negative.")
    start_price = signals_data['Close'].iloc[0]
    end_price = signals_data['Close'].iloc[-1]
    shares_bought = int(start_balance // start_price)
    amount_invested = shares_bought * start_price
    remaining_balance = start_balance - amount_invested
    final_value = shares_bought * end_price + remaining_balance
    return calculate_return(start_balance, final_value)

def calculate_buy_and_hold_values(signals_data: pd.DataFrame, start_balance: float) -> pd.DataFrame:
    """
    Calculate the portfolio values over time for a buy-and-hold strategy based on the provided market data.

    Args:
        signals_data (pd.DataFrame): A DataFrame containing market data with a 'Close' column.
        start_balance (float): The initial amount of money available for trading.

    Returns:
        pd.DataFrame: A DataFrame containing the portfolio value over time, along with the balance and number of shares held.

    Raises:
        ValueError: If the signals_data does not contain a 'Close' column or is empty or start balance is less than 0.
    """
    if start_balance < 0:
        raise ValueError("Starting balance cannot be negative.")
    if signals_data.empty:
        raise ValueError("signals_data is empty. Cannot calculate buy-and-hold values.")
    if 'Close' not in signals_data.columns:
        raise ValueError("signals_data must contain a 'Close' column")

    start_price = signals_data['Close'].iloc[0]
    shares_bought = int(start_balance // start_price)
    amount_invested = shares_bought * start_price
    remaining_balance = start_balance - amount_invested
    final_values = []
    for index, row in signals_data.iterrows():
        current_price = row['Close']
        final_value = shares_bought * current_price + remaining_balance
        final_values.append({
            'Date': index,
            'Portfolio Value': final_value,
            'Balance': remaining_balance,
            'Shares': shares_bought,
        })
    buy_and_hold_values = pd.DataFrame(final_values)
    return buy_and_hold_values