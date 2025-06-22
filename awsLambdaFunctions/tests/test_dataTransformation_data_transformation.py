import pytest
from unittest.mock import patch, MagicMock, mock_open
import json
import psycopg2
import dataTransformation.data_transformation as rl
from dataTransformation.data_transformation import run_data_transformation, lambda_handler, get_db_config_from_s3

MOCK_DB_CONFIG = {
    "DB_HOST": "test-host",
    "DB_PORT": "5432",
    "DB_NAME": "test-db",
    "DB_USER": "test-user",
    "DB_PASSWORD": "test-password"
}

@patch('dataTransformation.data_transformation.os')
@patch('dataTransformation.data_transformation.s3')
def test_get_db_config_from_s3(mock_s3, mock_os):
    mock_os.environ = {'BUCKET_NAME':'mock_bucket'}
    mock_response = MagicMock()
    mock_response['Body'].read.return_value = json.dumps(MOCK_DB_CONFIG).encode('utf-8')
    
    mock_s3.get_object.return_value = mock_response

    get_db_config_from_s3()
    assert rl.CONFIG == { "DB_HOST": "test-host", "DB_PORT": "5432", "DB_NAME": "test-db", "DB_USER": "test-user", "DB_PASSWORD": "test-password" }

@patch('dataTransformation.data_transformation.CONFIG')
@patch('dataTransformation.data_transformation.psycopg2')
# Tests for run_data_transformation
def test_run_data_transformation_success(mock_psycopg2, mock_config):
    """Test successful data transformation execution."""
    mock_config = MOCK_DB_CONFIG
    mock_db_connection = MagicMock()
    mock_cursor = MagicMock()
    
    mock_psycopg2.connect = mock_db_connection
    mock_db_connection.cursor = mock_cursor
    mock_cursor.fetchall.return_value = "dummy success"

    # Call the function
    run_data_transformation()
    
    # Verify database connection
    mock_db_connection.assert_called_once()

    # # Verify query execution
    mock_cursor = mock_db_connection.return_value.cursor.return_value
    mock_cursor.execute.assert_called_once_with("select transform_input()")

    mock_commit = mock_db_connection.return_value.commit
    mock_commit.assert_called_once()
    

@patch('dataTransformation.data_transformation.psycopg2')
def test_run_data_transformation_db_error(mock_psycopg2):
    """Test database connection error handling."""
    # Mock database connection error
    mock_psycopg2.connect.side_effect = psycopg2.Error("Connection failed")
    mock_db_connection = MagicMock()

    # Call the function
    run_data_transformation()

    # Verify error was handled (no exception raised)
    mock_db_connection.return_value.commit.assert_not_called()


if __name__ == '__main__':
    pytest.main([__file__])
