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

def get_file_name():
    file_name = "output_{}.txt".format(datetime.today().strftime("%Y%m%d"))
    return file_name

def get_client_sftp_metadata():
    #establish connection to rds
    db_host = CONFIG["DB_HOST"]
    db_port = CONFIG["DB_PORT"]
    db_name = CONFIG["DB_NAME"]
    db_user = CONFIG["DB_USER"]
    db_password = CONFIG["DB_PASSWORD"]

    client_metadata_query = "select sftp_directory from client_sftp_metadata"

    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        cursor = conn.cursor()
        cursor.execute(client_metadata_query)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
        print(str(e))
    client_sftp_list = [row[0] for row in rows]

    return client_sftp_list

def output_to_s3():
    #establish connection to rds
    db_host = CONFIG["DB_HOST"]
    db_port = CONFIG["DB_PORT"]
    db_name = CONFIG["DB_NAME"]
    db_user = CONFIG["DB_USER"]
    db_password = CONFIG["DB_PASSWORD"]

    file_name = get_file_name()
    client_sftp_directories = get_client_sftp_metadata()

    for client_dir in client_sftp_directories:
        output_data_query = f"""SELECT * from aws_s3.query_export_to_s3('select * from output_financial_data_vw', aws_commons.create_s3_uri('{CONFIG['S3_BUCKET']}', 'outputData/{client_dir}/{file_name}', 'ap-southeast-1') ,   options :='format csv, header true')""".format(file_name = file_name)
        print(output_data_query)

        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                dbname=db_name,
                user=db_user,
                password=db_password
            )
            cursor = conn.cursor()
            cursor.execute(output_data_query)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(str(e))

def lambda_handler(event, context):
    get_db_config_from_s3()
    output_to_s3()
    
    return {
        'statusCode': 200,
    }
