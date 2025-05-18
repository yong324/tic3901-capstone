import boto3
from datetime import datetime
import psycopg2

s3 = boto3.client('s3')

def get_file_name():
    """ 
    files will be name according to the date they were produced
    """
    output_file_name = "outputdata_{}.txt".format(datetime.today().strftime("%Y%m%d"))
    return output

def write_output_to_s3():
    db_host = "database-1.ct422ga2wer2.ap-southeast-1.rds.amazonaws.com"
    db_port = "5432"
    db_name = ""
    db_user = "postgres"
    db_password = "tic3901?!"

    file_name = get_file_name()
    query = ""

    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        print("successfully connected!")
        cursor = conn.cursor()
        cursor.execute("select * from customers limit 1")
        results = cursor.fetchall()
        print(results)
        
    except Exception as e:
        print(str(e))

    return

def lambda_handler(event, context):
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
