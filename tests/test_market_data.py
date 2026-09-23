import pytest
import pandas as pd
from src.data.market_data import get_market_data
from datetime import datetime, timedelta
from unittest.mock import patch

def test_invalid_date():
    with pytest.raises(ValueError, match="Start and end dates must be in 'YYYY-MM-DD' format"):
        get_market_data('AAPL', '2023-01-01', '2023-02-30')

@pytest.mark.parametrize("start, end", [
    ('2023-02-01', '2023-01-01'),
    ('2023-01-01', '2023-01-01')])
def test_start_date_after_or_equal_to_end_date(start, end):
    with pytest.raises(ValueError, match="Start date must be earlier than end date."):
        get_market_data('AAPL', start, end)

def test_end_date_in_future():
    future_date = datetime.now() + timedelta(days=1)
    with pytest.raises(ValueError, match="End date cannot be in the future."):
        get_market_data('AAPL', '2023-01-01', future_date.strftime('%Y-%m-%d'))

@pytest.mark.parametrize("ticker", ["", "   "])
def test_empty_ticker(ticker):
    with pytest.raises(ValueError, match="Ticker symbol cannot be empty."):
        get_market_data(ticker, '2023-01-01', '2023-02-01')

def test_no_data_found():
    with patch('src.data.market_data.yf.download', return_value=pd.DataFrame()):
        with pytest.raises(ValueError, match="No data found for ticker 'APPL' between 2023-01-01 and 2023-02-01."):
            get_market_data('APPL', '2023-01-01', '2023-02-01')

def test_successful_data_fetch():
    test_data = pd.DataFrame({
        'Open': [150, 152],
        'High': [155, 157],
        'Low': [149, 151],
        'Close': [154, 156],
        'Volume': [1000000, 1200000]
    })
    with patch('src.data.market_data.yf.download', return_value=test_data):
        result = get_market_data('AAPL', '2023-01-01', '2023-02-01')
        pd.testing.assert_frame_equal(result, test_data)

def test_runtime_error_on_fetch():
    with patch('src.data.market_data.yf.download', side_effect=Exception("Network error")):
        with pytest.raises(RuntimeError, match="Failed to fetch market data: Network error"):
            get_market_data('AAPL', '2023-01-01', '2023-02-01')