import json
import csv
import random
import string
import io
import boto3
from datetime import date
from datetime import datetime
import os

s3= boto3.client('s3')

def _generate_pid():
    """Generates a PID: an uppercase alphabet followed by 4 random integers."""
    return random.choice(string.ascii_uppercase) + "".join(random.choices(string.digits, k=4))

def _generate_data_row(trade_date_str):
    """Generates a single row of data."""
    pid = _generate_pid()
    region = random.choice(['A', 'E', 'N', 'S', 'F'])
    metric = random.randint(1, 500)
    alpha = round(random.uniform(0, 10), 3)
    delta = round(random.uniform(0, 10), 3)
    theta = round(random.uniform(-100, 100), 2)
    gamma = round(random.uniform(-200, 200), 3)
    rho = round(random.uniform(-50, 50), 3)
    return [trade_date_str, pid, region, metric, alpha, delta, theta, gamma, rho]

def generate_trade_data_csv(num_rows: int = 100):
    """
    Generates a CSV file with trade-like data.

    Args:
        num_rows (int): The number of data rows to generate.
    """
    header = [
        'trade_date', 'pid', 'region', 'metric',
        'alpha', 'delta', 'theta', 'gamma', 'rho'
    ]
    
    # Use the current date for all trade_date entries
    current_trade_date = trade_date = datetime.today().strftime('%Y-%m-%d')
        
    # Write the data rows
    data =[header]
    for _ in range(num_rows):
        row = _generate_data_row(current_trade_date)
        data.append(row)
            
    return data

def write_to_s3(data):
    trade_date = datetime.today().strftime('%Y%m%d')
    bucket = os.environ['BUCKET_NAME']
    key = f"inputData/input_{trade_date}.txt"

    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerows(data)

    print(f"Saving csv to {bucket}/{key}")
    s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
    


def lambda_handler(event, context):
    data = generate_trade_data_csv()
    write_to_s3(data)

    return {
        'statusCode': 200,
    }
