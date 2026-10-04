import pytest
import pandas as pd
from src.backtesting.backtester import calculate_buy_and_hold_return, run_backtest, calculate_return, calculate_buy_and_hold_values

def test_run_backtest_buy_and_sell():
    sample_data = {
        'Close': [100, 110, 120],
        'Signal': [1, 0, -1]
    }

    sample_df = pd.DataFrame(sample_data)
    result = run_backtest(sample_df, 1000)
    assert result['Portfolio Value'].tolist() == [1000, 1100, 1200]
    assert result['Balance'].tolist() == [0, 0, 1200]
    assert result['Shares'].tolist() == [10, 10, 0]

def test_run_backtest_no_buy_or_sell_signals():
    sample_data = {
        'Close': [100, 110, 120],
        'Signal': [0, 0, 0]
    }

    sample_df = pd.DataFrame(sample_data)
    result = run_backtest(sample_df, 1000)
    assert result['Portfolio Value'].tolist() == [1000, 1000, 1000]
    assert result['Balance'].tolist() == [1000, 1000, 1000]
    assert result['Shares'].tolist() == [0, 0, 0]

def test_run_backtest_sell_signal_without_shares():
    sample_data = {
        'Close': [100, 110, 120],
        'Signal': [0, -1, 0]
    }

    sample_df = pd.DataFrame(sample_data)
    result = run_backtest(sample_df, 1000)
    assert result['Portfolio Value'].tolist() == [1000, 1000, 1000]
    assert result['Balance'].tolist() == [1000, 1000, 1000]
    assert result['Shares'].tolist() == [0, 0, 0]

def test_run_backtest_leftover_balance_after_buy():
    sample_data = {
        'Close': [100, 110, 120],
        'Signal': [1, 0, 0]
    }

    sample_df = pd.DataFrame(sample_data)
    result = run_backtest(sample_df, 1050)
    assert result['Portfolio Value'].tolist() == [1050, 1150, 1250]
    assert result['Balance'].tolist() == [50, 50, 50]
    assert result['Shares'].tolist() == [10, 10, 10]

@pytest.mark.parametrize("label", [
    'Close',
    'Signal'
])
def test_run_backtest_missing_columns(label):
    with pytest.raises(ValueError, match=f"signals_data must contain a '{label}' column"):
        sample_data = {
            'Close': [100, 110, 120],
            'Signal': [1, 0, -1]
        }
        sample_df = pd.DataFrame(sample_data)
        sample_df.drop(columns=[label], inplace=True)
        run_backtest(sample_df, 1000)

def test_run_backtest_insufficient_balance_for_buy():
    sample_data = {
        'Close': [100, 110, 120],
        'Signal': [1, 0, 0]
    }

    sample_df = pd.DataFrame(sample_data)
    result = run_backtest(sample_df, 50)
    assert result['Portfolio Value'].tolist() == [50, 50, 50]
    assert result['Balance'].tolist() == [50, 50, 50]
    assert result['Shares'].tolist() == [0, 0, 0]

def test_calculate_return():
    start_value = 1000
    end_value = 1200
    expected_return = 20.0
    result = calculate_return(start_value, end_value)
    assert result == expected_return

def test_calculate_return_zero_start_value():
    start_value = 0
    end_value = 1200
    with pytest.raises(ValueError, match="Start value cannot be zero for return calculation."):
        calculate_return(start_value, end_value)

def test_calculate_return_unchanged_return():
    start_value = 1000
    end_value = 1000
    expected_return = 0.0
    result = calculate_return(start_value, end_value)
    assert result == expected_return

def test_calculate_return_negative_return():
    start_value = 1000
    end_value = 800
    expected_return = -20.0
    result = calculate_return(start_value, end_value)
    assert result == expected_return

def test_calculate_buy_and_hold_values():
    sample_data = {
        'Close': [100, 110, 120]
    }

    sample_df = pd.DataFrame(sample_data)
    start_balance = 1000
    result = calculate_buy_and_hold_values(sample_df, start_balance)
    assert result['Portfolio Value'].tolist() == [1000, 1100, 1200]
    assert result['Balance'].tolist() == [0, 0, 0]
    assert result['Shares'].tolist() == [10, 10, 10]

def test_calculate_buy_and_hold_values_empty_dataframe():
    empty_df = pd.DataFrame()
    start_balance = 1000
    with pytest.raises(ValueError, match="signals_data is empty. Cannot calculate buy-and-hold values."):
        calculate_buy_and_hold_values(empty_df, start_balance)

def test_calculate_buy_and_hold_values_missing_close_column():
    sample_data = {
        'Open': [100, 110, 120]
    }

    sample_df = pd.DataFrame(sample_data)
    start_balance = 1000
    with pytest.raises(ValueError, match="signals_data must contain a 'Close' column"):
        calculate_buy_and_hold_values(sample_df, start_balance)

def test_calculate_buy_and_hold_values_zero_start_balance():
    sample_data = {
        'Close': [100, 110, 120]
    }

    sample_df = pd.DataFrame(sample_data)
    start_balance = 0
    result = calculate_buy_and_hold_values(sample_df, start_balance)
    assert result['Portfolio Value'].tolist() == [0, 0, 0]
    assert result['Balance'].tolist() == [0, 0, 0]
    assert result['Shares'].tolist() == [0, 0, 0]

def test_calculate_buy_and_hold_values_insufficient_start_balance():
    sample_data = {
        'Close': [100, 110, 120]
    }

    sample_df = pd.DataFrame(sample_data)
    start_balance = 50
    result = calculate_buy_and_hold_values(sample_df, start_balance)
    assert result['Portfolio Value'].tolist() == [50, 50, 50]
    assert result['Balance'].tolist() == [50, 50, 50]
    assert result['Shares'].tolist() == [0, 0, 0]

def test_calculate_buy_and_hold_values_negative_start_balance():
    sample_data = {
        'Close': [100, 110, 120]
    }

    sample_df = pd.DataFrame(sample_data)
    start_balance = -100
    with pytest.raises(ValueError, match="Starting balance cannot be negative."):
        calculate_buy_and_hold_values(sample_df, start_balance)

def test_calculate_buy_and_hold_values_leftover_balance():
    sample_data = {
        'Close': [100, 110, 120]
    }

    sample_df = pd.DataFrame(sample_data)
    start_balance = 1050
    result = calculate_buy_and_hold_values(sample_df, start_balance)
    assert result['Portfolio Value'].tolist() == [1050, 1150, 1250]
    assert result['Balance'].tolist() == [50, 50, 50]
    assert result['Shares'].tolist() == [10, 10, 10]

def test_buy_and_hold_values_loss():
    sample_data = {
        'Close': [100, 90, 80]
    }

    sample_df = pd.DataFrame(sample_data)
    start_balance = 1000
    result = calculate_buy_and_hold_values(sample_df, start_balance)
    assert result['Portfolio Value'].tolist() == [1000, 900, 800]
    assert result['Balance'].tolist() == [0, 0, 0]
    assert result['Shares'].tolist() == [10, 10, 10]

def test_date_preservation_in_buy_and_hold_values():
    sample_data = {
        'Close': [100, 110, 120]
    }
    sample_df = pd.DataFrame(sample_data, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']))
    start_balance = 1000
    result = calculate_buy_and_hold_values(sample_df, start_balance)
    assert all(result['Date'] == sample_df.index)

def test_buy_and_hold_return():
    sample_data = {
        'Close': [100, 110, 120]
    }

    sample_df = pd.DataFrame(sample_data)
    start_balance = 1000
    result = calculate_buy_and_hold_return(sample_df, start_balance)
    assert result == 20.0

def test_buy_and_hold_return_loss():
    sample_data = {
        'Close': [100, 90, 80]
    }

    sample_df = pd.DataFrame(sample_data)
    start_balance = 1000
    result = calculate_buy_and_hold_return(sample_df, start_balance)
    assert result == -20.0

def test_buy_and_hold_return_missing_close_column():
    sample_data = {
        'Open': [100, 110, 120]
    }
    sample_df = pd.DataFrame(sample_data)
    start_balance = 1000
    with pytest.raises(ValueError, match="signals_data must contain a 'Close' column"):
        calculate_buy_and_hold_return(sample_df, start_balance)

def test_buy_and_hold_return_negative_start_balance():
    sample_data = {
        'Close': [100, 110, 120]
    }
    sample_df = pd.DataFrame(sample_data)
    start_balance = -1000
    with pytest.raises(ValueError, match="Starting balance cannot be negative."):
        calculate_buy_and_hold_return(sample_df, start_balance)

def test_buy_and_hold_return_zero_start_balance():
    sample_data = {
        'Close': [100, 110, 120]
    }

    with pytest.raises(ValueError, match="Starting balance cannot be zero."):
        calculate_buy_and_hold_return(pd.DataFrame(sample_data), 0)

def test_buy_and_hold_return_empty_dataframe():
    empty_df = pd.DataFrame()
    start_balance = 1000
    with pytest.raises(ValueError, match="signals_data is empty. Cannot calculate buy-and-hold return."):
        calculate_buy_and_hold_return(empty_df, start_balance)