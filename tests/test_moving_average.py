import pytest
import pandas as pd
from src.strategy.moving_average import calculate_moving_averages, generate_signals

def test_calculate_moving_average():
    sample_data = pd.DataFrame({'Close': [100, 110, 120, 130, 140]})
    result = calculate_moving_averages(sample_data, short_window=5, long_window=20)
    assert 'Short_MA' in result.columns
    assert 'Long_MA' in result.columns
    assert result['Short_MA'].iloc[-1] == pytest.approx(120)
    assert result['Long_MA'].isna().all()

def test_calculate_moving_average_non_int_window():
    sample_data = pd.DataFrame({'Close': [100, 110, 120, 130, 140]})
    with pytest.raises(ValueError, match="Window sizes must be integers."):
        calculate_moving_averages(sample_data, short_window=5.5, long_window=20)

def test_calculate_moving_average_negative_window():
    sample_data = pd.DataFrame({'Close': [100, 110, 120, 130, 140]})
    with pytest.raises(ValueError, match="Window sizes must be positive integers."):
        calculate_moving_averages(sample_data, short_window=-5, long_window=20)

def test_calculate_moving_average_short_window_greater_than_long_window():
    sample_data = pd.DataFrame({'Close': [100, 110, 120, 130, 140]})
    with pytest.raises(ValueError, match="Short window must be less than long window."):
        calculate_moving_averages(sample_data, short_window=20, long_window=10)

def test_generate_signals_with_crossovers():
    sample_data = pd.DataFrame({'Close': [100, 110, 120, 130, 140, 130, 120, 110, 100]})
    ma_data = calculate_moving_averages(sample_data, short_window=2, long_window=3)
    result = generate_signals(ma_data)
    assert 'Signal' in result.columns
    assert not (result['Signal'] == 0).all()

def test_no_crossovers():
    sample_data = pd.DataFrame({'Close': [100, 110, 120, 130, 140]})
    ma_data = calculate_moving_averages(sample_data, short_window=2, long_window=3)
    result = generate_signals(ma_data)
    assert 'Signal' in result.columns
    assert (result['Signal'] == 0).all()

def test_not_enough_data_for_signals():
    sample_data = pd.DataFrame({'Close': [100, 120]})
    ma_data = calculate_moving_averages(sample_data, short_window=2, long_window=3)
    result = generate_signals(ma_data)
    assert 'Signal' in result.columns
    assert (result['Signal'] == 0).all()