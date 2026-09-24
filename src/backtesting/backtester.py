import pandas as pd
from src.trading.trading_engine import TradingEngine

def run_backtest(signals_data: pd.DataFrame, start_balance: float) -> pd.DataFrame:
    """
    Run a backtest using the provided signals data and starting balance.

    Parameters:
        signals_data (pd.DataFrame): A pandas DataFrame containing market data with 'Signal' column (generated from passing market data through the generate_signals function).
        start_balance (float): The initial amount of money available for trading.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the portfolio value over time, along with the balance and number of shares held.

    Raises:
        ValueError: If signals_data does not contain the required 'Signal' and 'Close' columns.
    """
    if 'Signal' not in signals_data.columns:
        raise ValueError("signals_data must contain a 'Signal' column")
    if 'Close' not in signals_data.columns:
        raise ValueError("signals_data must contain a 'Close' column")

    portfolio_history = []
    engine = TradingEngine(start_balance)
    for index, row in signals_data.iterrows():
        price = row['Close']
        if row['Signal'] == 1:
            shares_to_buy = int(engine.balance // price)
            if shares_to_buy > 0:
                engine.buy(price, shares_to_buy)
        elif row['Signal'] == -1:
            shares_to_sell = engine.shares
            if shares_to_sell > 0:
                engine.sell(price, shares_to_sell)
        portfolio_value = engine.get_portfolio_value(price)
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
    """
    start_price = signals_data['Close'].iloc[0]
    end_price = signals_data['Close'].iloc[-1]
    shares_bought = int(start_balance // start_price)
    amount_invested = shares_bought * start_price
    remaining_balance = start_balance - amount_invested
    final_value = shares_bought * end_price + remaining_balance
    return calculate_return(start_balance, final_value)