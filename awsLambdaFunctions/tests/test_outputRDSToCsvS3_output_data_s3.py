import pytest
from unittest.mock import patch, MagicMock, call
from datetime import datetime
import json
import psycopg2
import outputRDSToCsvS3.output_data_s3 as rl
from outputRDSToCsvS3.output_data_s3 import (
    get_file_name,
    get_client_sftp_metadata,
    output_to_s3,
    lambda_handler,
    get_db_config_from_s3
)


MOCK_DB_CONFIG = {
    "DB_HOST": "test-host",
    "DB_PORT": "5432",
    "DB_NAME": "test-db",
    "DB_USER": "test-user",
    "DB_PASSWORD": "test-password",
    "S3_BUCKET":"dummy_bucket"
}

@patch('outputRDSToCsvS3.output_data_s3.os')
@patch('outputRDSToCsvS3.output_data_s3.s3')
def test_get_db_config_from_s3(mock_s3, mock_os):
    mock_os.environ = {"BUCKET_NAME":"mock_bucket"}
    mock_response = MagicMock()
    mock_response['Body'].read.return_value = json.dumps(MOCK_DB_CONFIG).encode('utf-8')
    
    mock_s3.get_object.return_value = mock_response

    get_db_config_from_s3()
    rl.CONFIG == { "DB_HOST": "test-host", "DB_PORT": "5432", "DB_NAME": "test-db", "DB_USER": "test-user", "DB_PASSWORD": "test-password", "S3_BUCKET":"dummy_bucket" }


@patch('outputRDSToCsvS3.output_data_s3.datetime')
def test_get_file_name(mock_datetime):
    """Test file name generation."""
    mock_datetime.today.return_value = datetime(2025,1,1)

    file_name = get_file_name()
    assert file_name == f"output_20250101.txt"

# Tests for get_client_sftp_metadata
@patch('outputRDSToCsvS3.output_data_s3.CONFIG')
@patch('outputRDSToCsvS3.output_data_s3.psycopg2')
def test_get_client_sftp_metadata(mock_psycopg2, mock_config):
    """Test successful retrieval of client SFTP metadata."""
    # Mock database response
    mock_config = MOCK_DB_CONFIG
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_psycopg2.connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ('dir1',),
        ('dir2',),
        ('dir3',)
    ]

    # Call function
    result = get_client_sftp_metadata()

    # Verify database connection
    mock_psycopg2.connect.assert_called_once()

    # Verify query execution
    mock_cursor.execute.assert_called_once_with(
        "select sftp_directory from client_sftp_metadata"
    )

    # Verify result
    assert result == ['dir1', 'dir2', 'dir3']

# Tests for output_to_s3
@patch('outputRDSToCsvS3.output_data_s3.get_file_name')
@patch('outputRDSToCsvS3.output_data_s3.get_client_sftp_metadata')
@patch('outputRDSToCsvS3.output_data_s3.CONFIG')
@patch('outputRDSToCsvS3.output_data_s3.psycopg2')
def test_output_to_s3_success(mock_psycopg2, mock_config, mock_get_client_sftp_metadata, mock_get_file_name):
    """Test successful output to S3."""

    mock_config = MOCK_DB_CONFIG
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_psycopg2.connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_get_client_sftp_metadata.return_value = ["client_dir1","client_dir2","client_dir3"]
    mock_get_file_name.return_value = "file_name.csv"

    # Call function
    output_to_s3()

    # Verify database connections
    assert mock_psycopg2.connect.call_count == 3  # One for each directory

    # Verify query execution
    assert mock_cursor.execute.call_count == 3

# # Tests for lambda_handler
# @patch('outputRDSToCsvS3.output_data_s3.output_to_s3')
# def test_lambda_handler(mock_output_to_s3):
#     """Test successful lambda handler execution."""
#     mock_event = MagicMock()
#     mock_context = MagicMock()
#     response = lambda_handler(mock_event, mock_context)

#     mock_output_to_s3.assert_called_once()

#         # Verify response
#     assert response == {'statusCode': 200}

if __name__ == '__main__':
    pytest.main([__file__])

