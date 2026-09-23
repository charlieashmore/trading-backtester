import yfinance as yf
import pandas as pd
from datetime import datetime

def get_market_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Fetches market data for a given ticker symbol between specified start and end dates.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple).
        start (str): The start date in 'YYYY-MM-DD' format.
        end (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        pandas.DataFrame: A DataFrame containing the market data.

    Raises:
        ValueError: If the dates are invalid, incorrectly ordered, or in the future, if the ticker symbol is empty, or if no market data is found for the specified ticker and date range.
        RuntimeError: If there is an issue fetching data from Yahoo Finance.
    """
    datetime_format = "%Y-%m-%d"
    try:
        start_date = datetime.strptime(start, datetime_format)
        end_date = datetime.strptime(end, datetime_format)
    except ValueError:
        raise ValueError("Start and end dates must be in 'YYYY-MM-DD' format, and be valid dates.") from None

    if start_date >= end_date:
        raise ValueError("Start date must be earlier than end date.")

    if datetime.now() < end_date:
        raise ValueError("End date cannot be in the future.")

    ticker = ticker.strip()
    if not ticker:
        raise ValueError("Ticker symbol cannot be empty.")

    try:
        data = yf.download(ticker, start=start_date, end=end_date)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch market data: {e}")

    if data.empty:
        raise ValueError(f"No data found for ticker '{ticker}' between {start} and {end}.")

    return data