

from typing import Text
from bs4 import BeautifulSoup
import argparse
import requests
import json
from datetime import date


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
    price = get_stock(exchange, symbol)
    data = {
        'date': date.today().strftime('%Y-%m-%d'),
        'exchange': exchange,
        'symbol': symbol,
        'price': price
    }
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(data)
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


def run():
    parser = argparse.ArgumentParser(description='get stock value')
    parser.add_argument('--exchange', required=True,
                        type=Text, help='exchange code')
    parser.add_argument('--symbol', required=True,
                        type=Text, help='stock symbol')

    args = parser.parse_args()
    exchange = args.exchange
    symbol = args.symbol
    price = get_stock(exchange, symbol)
    data = {
        'date': date.today().strftime('%Y-%m-%d'),
        'exchange': exchange,
        'symbol': symbol,
        'price': price
    }
    return data
