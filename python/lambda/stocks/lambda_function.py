

from typing import Text
from bs4 import BeautifulSoup
import argparse
import requests
import json
from datetime import date
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = 'croesus'
HOST = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com'


def lambda_handler(event, context):
    if not 'pathParameters' in event:
        return {
            'statusCode': 400,
            'body': {'message': 'no pathParameters'}
        }
    parameters = event['pathParameters']
    if not 'symbol' in parameters:
        return {
            'statusCode': 400,
            'body': {'message': 'no symbol'}
        }
    if not 'exchange' in parameters:
        return {
            'statusCode': 400,
            'body': {'message': 'no exchange'}
        }
    exchange = parameters['exchange']
    symbol = parameters['symbol']
    cached = False
    print(event)
    if 'queryStringParameters' in event:
        print(event['queryStringParameters'])
        if 'cached' in event['queryStringParameters']:
            print(event['queryStringParameters']['cached'])
            cached = event['queryStringParameters']['cached']
    if cached:
        price = get_cached_stock(exchange, symbol)
    else:
        price = get_stock(exchange, symbol)
    if not price:
        return response(404, 'price for {}.{} not found, cached={}'.format(exchange, symbol, cached))
    data = {
        'date': date.today().strftime('%Y-%m-%d'),
        'exchange': exchange,
        'symbol': symbol,
        'price': price
    }
    return response(200, data)


def response(code, body):
    return {
        'statusCode': code,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(body)
    }


def get_nzx_stock(symbol):
    page = requests.get('https://www.nzx.com/instruments/{}/'.format(symbol))
    soup = BeautifulSoup(page.content, 'html.parser')
    h1 = soup.find_all('h1')
    price = h1[1].text.strip().replace('$', '')
    return float(price)


def get_stock(exchange, symbol):
    if exchange.lower() == 'nzx':
        return get_nzx_stock(symbol)
    raise Exception('invalid exchange ' + exchange)


def get_cached_stock(exchange, symbol):
    s3_client = boto3.client('s3')
    KEY_NAME = 'prices.json'
    FILE_NAME = '/tmp/' + KEY_NAME

    price_data = {}
    try:
        s3_client.download_file(BUCKET_NAME, KEY_NAME, FILE_NAME)
        with open(FILE_NAME, 'r') as input:
            price_data = json.load(input)
    except ClientError as e:
        print('error : {}'.format(e))
        pass

    print(price_data)
    price = None
    if exchange in price_data:
        if symbol in price_data[exchange]:
            price = price_data[exchange][symbol]
    return price
