import boto3
import json
import os
from botocore.exceptions import ClientError
import dateparser

BUCKET_NAME = 'croesus'

# better error handling
# write to logs


def response(code, body):
    return {
        'statusCode': code,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(body)
    }


def lambda_handler(event, context):

    if not 'pathParameters' in event:
        method = event['requestContext']['http']['method']
        if method == 'GET':
            return get_total_response()
        return response(405, {'error': 'unhandled method'})

    method = event['requestContext']['http']['method']
    parameters = event['pathParameters']

    if method == 'GET':
        return get(parameters)
    if method == 'POST':
        return post(parameters, json.loads(event['body']))
    return response(405, {'error': 'unhandled method'})


def get(parameters):
    if 'symbol' in parameters:
        return get_symbol_response(parameters)
    if 'exchange' in parameters:
        return get_exchange_response(parameters)
    return get_total_response(parameters)


def post(parameters, body):
    if 'symbol' in parameters:
        return post_symbol(parameters, body)


def post_symbol(parameters, body):
    exchange = parameters['exchange']
    symbol = parameters['symbol']
    date = body['date']
    quantity = body['quantity']
    price = body['price']
    return response(200, add_transaction(exchange, symbol, date, quantity, price))


def add_transaction(exchange, symbol, date, quantity, price):
    s3_client = boto3.client('s3')
    KEY_NAME = 'transactions.json'
    FILE_NAME = '/tmp/' + KEY_NAME

    transactions = []
    try:
        s3_client.download_file(BUCKET_NAME, KEY_NAME, FILE_NAME)
        with open(FILE_NAME, 'r') as input:
            transactions = json.load(input)
    except ClientError as e:
        pass

    # sort out the date format
    date_value = dateparser.parse(date)
    formatted_date = date_value.strftime('%Y-%m-%d')
    transaction = {
        'exchange': exchange,
        'symbol': symbol,
        'date': formatted_date,
        'quantity': quantity,
        'price': price,
    }
    transactions.append(transaction)

    with open(FILE_NAME, 'w') as output:
        json.dump(transactions, output)

    try:
        response = s3_client.upload_file(FILE_NAME, BUCKET_NAME, KEY_NAME)
    except ClientError as e:
        print(e)

    os.remove(FILE_NAME)

    return transactions


def get_total_response():
    return response(200, get_transactions(None, None))


def get_exchange_response(parameters):
    exchange = parameters['exchange']
    return response(200, get_transactions(exchange, None))


def get_symbol_response(parameters):
    exchange = parameters['exchange']
    symbol = parameters['symbol']
    return response(200, get_transactions(exchange, symbol))


def get_transactions(exchange, symbol):
    s3_client = boto3.client('s3')
    KEY_NAME = 'transactions.json'
    FILE_NAME = '/tmp/' + KEY_NAME

    transactions = []
    try:
        s3_client.download_file(BUCKET_NAME, KEY_NAME, FILE_NAME)
        with open(FILE_NAME, 'r') as input:
            transactions = json.load(input)
    except ClientError as e:
        pass

    if exchange is None:
        return transactions

    exchange_transactions = [
        t for t in transactions if t['exchange'] == exchange]

    if symbol is None:
        return exchange_transactions

    symbol_transactions = [
        t for t in exchange_transactions if t['symbol'] == symbol]

    return symbol_transactions
