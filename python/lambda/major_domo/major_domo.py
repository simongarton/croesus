import boto3
import json
from botocore.exceptions import ClientError

BUCKET_NAME = 'croesus'

# better error handling
# logs


def response(code, body):
    return {
        'statusCode': code,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(body)
    }


def save_price(exchange, symbol, price):
    s3_client = boto3.client('s3')
    FILE_NAME = 'prices.json'

    price_data = {}
    try:
        s3_client.download_file(BUCKET_NAME, FILE_NAME, FILE_NAME)
        with open(FILE_NAME, 'r') as input:
            price_data = json.load(input)
    except ClientError as e:
        pass

    if not exchange in price_data:
        price_data[exchange] = {}
    price_data[exchange][symbol] = price

    with open(FILE_NAME, 'w') as output:
        json.dump(price_data, output)

    try:
        response = s3_client.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
    except ClientError as e:
        print(e)

    return price_data


def save_price_history(exchange, symbol, date, price):

    s3_client = boto3.client('s3')
    FILE_NAME = 'price_history.json'

    price_data = {}
    try:
        s3_client.download_file(BUCKET_NAME, FILE_NAME, FILE_NAME)
        with open(FILE_NAME, 'r') as input:
            price_data = json.load(input)
    except ClientError as e:
        pass

    if not exchange in price_data:
        price_data[exchange] = {}
    if not symbol in price_data[exchange]:
        price_data[exchange][symbol] = {}
    price_data[exchange][symbol][date] = price

    with open(FILE_NAME, 'w') as output:
        json.dump(price_data, output)

    try:
        response = s3_client.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
    except ClientError as e:
        print(e)

    return price_data


def test():
    response1 = save_price('NZX', 'XXX', 1.02)
    response2 = save_price_history('NZX', 'XXX', '2021-02-21', 1.02)
    data = {
        'response1': response1,
        'response2': response2
    }
    print(data)
    return response(200, data)


# test()
