import boto3
from datetime import datetime
import psycopg2
import json
import os

s3 = boto3.client('s3')

def get_db_config_from_s3():
    response = s3.get_object(Bucket=os.environ['BUCKET_NAME'], Key="config/dbconfig.json")
    config_data = response['Body'].read().decode('utf-8')
    db_config = json.loads(config_data)
    global CONFIG 
    CONFIG = db_config


def run_data_transformation():
    #establish connection to rds
    db_host = CONFIG["DB_HOST"]
    db_port = CONFIG["DB_PORT"]
    db_name = CONFIG["DB_NAME"]
    db_user = CONFIG["DB_USER"]
    db_password = CONFIG["DB_PASSWORD"]

    data_transformation_query = "select transform_input()"

    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        cursor = conn.cursor()
        cursor.execute(data_transformation_query)
        conn.commit()
        
    except Exception as e:
        print(str(e))

    return 1

def lambda_handler(event, context):
    get_db_config_from_s3()
    run_data_transformation()
    return {
        'statusCode': 200,
    }
