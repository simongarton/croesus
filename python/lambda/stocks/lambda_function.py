

from typing import Text
from bs4 import BeautifulSoup
import os
import requests
import json
from datetime import date
from botocore.exceptions import ClientError
import psycopg2

HOST = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com'


def response(code, body):
    return {
        'statusCode': code,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(body)
    }


def get_database_connection():
    try:
        dbname = os.environ.get('PGDATABASE')
        user = os.environ.get('PGUSER')
        host = os.environ.get('PGHOST')
        password = os.environ.get('PGPASSWORD')
        connection = "dbname='{}' user='{}' host='{}' password='{}'".format(
            dbname, user, host, password)
        conn = psycopg2.connect(connection)
        return conn
    except:
        return {
            'statusCode': 500,
            'body': json.dumps('connection error : {}'.format(sys.exc_info()[0]))
        }


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
    if 'queryStringParameters' in event:
        print(event['queryStringParameters'])
        if 'cached' in event['queryStringParameters']:
            print(event['queryStringParameters']['cached'])
            cached = event['queryStringParameters']['cached']
    if cached:
        price = get_cached_stock(exchange, symbol)
        if price == None:
            return response(404, '{}:{} not found'.format(exchange, symbol))
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


def getRandomUserAgent():
    uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
                 "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
                 "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
                 "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
                 "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
                 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"
                 ]


def get_nzx_stock(symbol):
    headers = {'User-Agent': getRandomUserAgent()}
    page = requests.get(
        'https://www.nzx.com/instruments/{}/'.format(symbol), headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    h1 = soup.find_all('h1')
    price = h1[1].text.strip().replace('$', '')
    return float(price)


def get_stock(exchange, symbol):
    if exchange.lower() == 'nzx':
        return get_nzx_stock(symbol)
    raise Exception('invalid exchange ' + exchange)


def get_cached_stock(exchange, symbol):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute('SELECT id, exchange, symbol, price FROM price WHERE exchange = %s AND symbol = %s',
                [
                    exchange,
                    symbol
                ])
    rows = cur.fetchall()
    if len(rows) == 0:
        return None
    return rows[0][3]
