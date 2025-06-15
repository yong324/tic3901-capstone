import pytest
from unittest.mock import patch, MagicMock
import json
import psycopg2
import inputCsvToRDS.lambda_function as rl # for testing of global variables
from inputCsvToRDS.lambda_function import (
    get_latest_input_data_filename,
    read_latest_file_to_rds,
    lambda_handler,
    get_db_config_from_s3
)

MOCK_DB_CONFIG = {
    "DB_HOST": "test-host",
    "DB_PORT": "5432",
    "DB_NAME": "test-db",
    "DB_USER": "test-user",
    "DB_PASSWORD": "test-password",
    "S3_BUCKET": "mock_bucket"
}

@patch('inputCsvToRDS.lambda_function.os')
@patch('inputCsvToRDS.lambda_function.s3')
def test_get_db_config_from_s3(mock_s3, mock_os):
    mock_os.environ = {"BUCKET_NAME":"mock_bucket"}
    mock_response = MagicMock()
    mock_response['Body'].read.return_value = json.dumps(MOCK_DB_CONFIG).encode('utf-8')
    
    mock_s3.get_object.return_value = mock_response

    get_db_config_from_s3()
    assert rl.CONFIG == { "DB_HOST": "test-host", "DB_PORT": "5432", "DB_NAME": "test-db", "DB_USER": "test-user", "DB_PASSWORD": "test-password","S3_BUCKET": "mock_bucket" }


# Tests for get_latest_input_data_filename
@patch('inputCsvToRDS.lambda_function.s3')
def test_get_latest_input_data_filename(mock_s3):
    """Test successful retrieval of latest input data filename."""
    # Mock S3 response
    
    mock_s3.list_objects_v2.return_value = {
        'Contents': [
            {'Key': 'inputData/file1.csv', 'LastModified': '2023-01-01'},
            {'Key': 'inputData/file2.csv', 'LastModified': '2023-01-02'},
            {'Key': 'inputData/file3.csv', 'LastModified': '2023-01-03'}
        ]
    }

    # Call function
    result = get_latest_input_data_filename('test-bucket', 'inputData/')

    # Verify S3 call
    mock_s3.list_objects_v2.assert_called_once_with(
        Bucket='test-bucket',
        Prefix='inputData/'
    )

    # Verify result
    assert result == 'inputData/file3.csv'

# Tests for read_latest_file_to_rds
@patch('inputCsvToRDS.lambda_function.CONFIG')
@patch('inputCsvToRDS.lambda_function.psycopg2')
def test_read_latest_file_to_rds_success(mock_psycopg2,mock_config):
    """Test successful reading of latest file to RDS."""
    # Mock database response
    mock_config.return_value = MOCK_DB_CONFIG

    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_psycopg2.connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = "dummy success"
    # mock_boto3.return_value = MagicMock()
    
    # Call function
    read_latest_file_to_rds('inputData/test.csv')

    # Verify database connection
    mock_psycopg2.connect.assert_called_once()

    # Verify query execution
    mock_cursor.execute.assert_called_once()
    mock_psycopg2.connect.return_value.commit.assert_called_once()

@patch('inputCsvToRDS.lambda_function.psycopg2')
def test_read_latest_file_to_rds_error(mock_psycopg2):
    """Test error handling in read_latest_file_to_rds."""
    mock_psycopg2.connect.side_effect = Exception("Database error")

    # Call function
    read_latest_file_to_rds('inputData/test.csv')

    # Verify error was handled gracefully
    mock_psycopg2.connect.return_value.commit.assert_not_called()

# # Tests for lambda_handler
# @patch('inputCsvToRDS.lambda_function.get_latest_input_data_filename')
# @patch('inputCsvToRDS.lambda_function.read_latest_file_to_rds')
# def test_lambda_handler(mock_read_latest_file_to_rds,mock_get_latest_input_data_filename):
#     """Test successful lambda handler execution."""
#     # Mock S3 response for get_latest_input_data_filename

#     mock_get_latest_input_data_filename.return_value = "dummy_location"
#     mock_event = MagicMock()
#     mock_context = MagicMock()

#     response = lambda_handler(mock_event, mock_context)

#     mock_get_latest_input_data_filename.assert_called_once_with('tic4303-capstone','inputData/')
#     mock_read_latest_file_to_rds.assert_called_once_with("dummy_location")
    
#     # Verify response
#     assert response == {'statusCode': 200}

if __name__ == '__main__':
    pytest.main([__file__])
    