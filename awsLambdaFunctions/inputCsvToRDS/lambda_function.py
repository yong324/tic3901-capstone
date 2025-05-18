import boto3
from datetime import datetime
import psycopg2
import json

s3 = boto3.client('s3')
response = s3.get_object(Bucket="tic4303-capstone", Key="config/dbconfig.json")
config_data = response['Body'].read().decode('utf-8')
CONFIG = json.loads(config_data)

# test comment to test deployment

def get_latest_input_data_filename(bucket_name, prefix):
    # Retrieve the list of objects
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
    # Extract and sort objects by 'LastModified'
    objects = sorted(response['Contents'], key=lambda obj: obj['LastModified'])
    
    # Format the output for each object
    latest_object_location = objects[-1]['Key']

    return latest_object_location

def read_latest_file_to_rds(latest_object_location):
    #establish connection to rds
    db_host = CONFIG["DB_HOST"]
    db_port = CONFIG["DB_PORT"]
    db_name = CONFIG["DB_NAME"]
    db_user = CONFIG["DB_USER"]
    db_password = CONFIG["DB_PASSWORD"]

    query = "SELECT aws_s3.table_import_from_s3('input_financial_data','','(format csv, header true)','tic4303-capstone','{file_location}','ap-southeast-1')".format(file_location = latest_object_location)

    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.commit()
        
    except Exception as e:
        print(str(e))

    return

def lambda_handler(event, context):
    bucket_name = 'tic4303-capstone'
    prefix = 'inputData/'  # Replace with the directory path you want to list

    latest_object_location = get_latest_input_data_filename(bucket_name, prefix)
    read_latest_file_to_rds(latest_object_location)

    return {
        'statusCode': 200,
    }
