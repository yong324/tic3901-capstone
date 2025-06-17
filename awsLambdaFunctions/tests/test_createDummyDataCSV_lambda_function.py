import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import json
import io
import csv
from createDummyDataCSV.lambda_function import (
    _generate_pid,
    _generate_data_row,
    generate_trade_data_csv,
    write_to_s3,
    lambda_handler
)

# Fixtures
@pytest.fixture
def today():
    return datetime.today().strftime('%Y-%m-%d')

# Tests for _generate_pid
def test_generate_pid_format():
    """Test PID generation format."""
    pid = _generate_pid()
    assert pid[0].isupper()
    assert pid[1:].isdigit()
    assert len(pid) == 5

def test_generate_pid_randomness():
    """Test PID generation randomness."""
    pids = set(_generate_pid() for _ in range(100))
    assert len(pids) > 1  # Should generate different PIDs

# Tests for _generate_data_row
def test_generate_data_row_structure(today):
    """Test data row structure."""
    row = _generate_data_row(today)
    assert len(row) == 9
    assert row[0] == today  # trade_date

def test_generate_data_row_value_ranges():
    """Test data row value ranges."""
    row = _generate_data_row(datetime.today().strftime('%Y-%m-%d'))
    
    assert row[2] in ['A', 'E', 'N', 'S', 'F']  # region
    assert 1 <= row[3] <= 500  # metric
    assert 0 <= row[4] <= 10  # alpha
    assert 0 <= row[5] <= 10  # delta
    assert -100 <= row[6] <= 100  # theta
    assert -200 <= row[7] <= 200  # gamma
    assert -50 <= row[8] <= 50  # rho

# Tests for generate_trade_data_csv
def test_generate_trade_data_csv_default():
    """Test CSV generation with default row count."""
    data = generate_trade_data_csv()
    assert len(data) == 101  # header + 100 rows

def test_generate_trade_data_csv_custom():
    """Test CSV generation with custom row count."""
    data = generate_trade_data_csv(5)
    assert len(data) == 6  # header + 5 rows

def test_generate_trade_data_csv_header():
    """Test CSV header format."""
    data = generate_trade_data_csv()
    expected_header = [
        'trade_date', 'pid', 'region', 'metric',
        'alpha', 'delta', 'theta', 'gamma', 'rho'
    ]
    assert data[0] == expected_header

def test_generate_trade_data_csv_row_format():
    """Test CSV data row format."""
    data = generate_trade_data_csv(1)
    assert len(data[1]) == 9

@patch('createDummyDataCSV.lambda_function.os')
@patch('createDummyDataCSV.lambda_function.s3')
@patch('createDummyDataCSV.lambda_function.datetime')
# Tests for write_to_s3
def test_write_to_s3(mock_datetime,mock_s3, mock_os):
    """Test S3 write functionality."""
    mock_os.environ = {"BUCKET_NAME": "mock_bucket"}
    mock_s3.put_object = MagicMock()
    mock_datetime.today.return_value = datetime(2025, 1, 1)

    test_data = [
        ['header1', 'header2'],
        ['data1', 'data2']
    ]
    
    write_to_s3(test_data)
    
    # Verify S3 put_object was called
    mock_s3.put_object.assert_called_once()
    
    # # Verify bucket and key
    call_args = mock_s3.put_object.call_args[1]
    assert call_args['Bucket'] == 'mock_bucket'
    assert call_args['Key'] == f'inputData/input_20250101.txt'
    
if __name__ == '__main__':
    pytest.main([__file__])
