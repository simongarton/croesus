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
    print(event)

    if not 'queryStringParameters' in event:
        return response(400, {'error': 'must include query parameter for date (1)'})
    if not 'date' in event['queryStringParameters']:
        return response(400, {'error': 'must include query parameter for date (2)'})

    query_date = dateparser.parse(event['queryStringParameters']['date'])
    if not 'pathParameters' in event:
        method = event['requestContext']['http']['method']
        if method == 'GET':
            return get_total_response(query_date)
        return response(405, {'error': 'unhandled method'})

    method = event['requestContext']['http']['method']
    parameters = event['pathParameters']

    if method == 'GET':
        return get(parameters, query_date)
    return response(405, {'error': 'unhandled method'})


def get(parameters, query_date):
    if 'symbol' in parameters:
        return get_symbol_response(parameters, query_date)
    if 'exchange' in parameters:
        return get_exchange_response(parameters, query_date)
    return get_total_response(query_date)


def get_total_response(query_date):
    return response(200, get_holdings(None, None, query_date))


def get_exchange_response(parameters, query_date):
    exchange = parameters['exchange']
    return response(200, get_holdings(exchange, None, query_date))


def get_symbol_response(parameters, query_date):
    exchange = parameters['exchange']
    symbol = parameters['symbol']
    return response(200, get_holdings(exchange, symbol, query_date))


def get_holdings(exchange, symbol, query_date):
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

    holdings_map = {}

    print('{} {} {}'.format(exchange, symbol, query_date))

    for transaction in transactions:
        print(transaction)
        transaction_date = dateparser.parse(transaction['date'])
        key = 'total'
        if transaction_date > query_date:
            print('out of date range {} > {}'.format(
                transaction_date, query_date))
            continue
        if exchange is not None:
            key = exchange
            if transaction['exchange'] != exchange:
                print('failed exchange {} != {}'.format(
                    transaction['exchange'], exchange))
                continue
        if symbol is not None:
            key = exchange + ':' + symbol
            if transaction['symbol'] != symbol:
                print('failed symbol {} != {}'.format(
                    transaction['symbol'], symbol))
                continue
        if not key in holdings_map:
            holdings_map[key] = 0
        print('adding {}:{}'.format(key, transaction['quantity']))
        holdings_map[key] = holdings_map[key] + transaction['quantity']

    holdings = []
    for key, value in holdings_map.items():
        holdings.append({'holding': key,
                         'quantity': value})

    # sort
    return holdings
