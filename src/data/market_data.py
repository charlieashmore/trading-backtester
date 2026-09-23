import yfinance as yf
import pandas as pd

def get_market_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Fetches market data for a given ticker symbol between specified start and end dates.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple).
        start (str): The start date in 'YYYY-MM-DD' format.
        end (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        pandas.DataFrame: A DataFrame containing the market data.
    """
    data = yf.download(ticker, start=start, end=end)
    return data