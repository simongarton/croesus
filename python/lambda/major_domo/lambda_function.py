import re
import boto3
import json
from botocore.exceptions import ClientError
import requests
import datetime
import random
import time
import os
import psycopg2
import sys


BUCKET_NAME = 'croesus'
HOST = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com'


# better error handling
# logs


def lambda_handler(event, context):

    # need to GET my list of holdings from
    # https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/holdings/nzx/test?date=2021-03-10
    # for the current day (think API key)
    # then iterate over each, with delays, calling the stocks lambda for each and updating price
    # and price history

    # I have to do the current day's holdings as I only can get new prices for the current day

    todays_date = datetime.datetime.now().strftime('%Y-%m-%d')
    holdings_response = requests.get(
        '{}/holdings?date={}'.format(HOST, todays_date))
    if holdings_response.status_code != 200:
        print(holdings_response)
        return response(holdings_response.status_code, holdings_response.text)

    updates = 0
    print(holdings_response.json())
    for holding in holdings_response.json():
        exchange = holding['exchange']
        symbol = holding['symbol']
        price = get_price(exchange, symbol)
        if not price:
            print('not saving ')
            continue
        print('saving {}.{} at {}'.format(exchange, symbol, price))
        save_price(exchange, symbol, price)
        save_price_history(exchange, symbol, todays_date, price)
        updates = updates + 1
        time.sleep(random.randint(0, 20)/10.0)

    return response(200, {'message': '{} prices updated'.format(updates)})


def get_price(exchange, symbol):
    price_response = requests.get(
        '{}/stocks/{}/{}'.format(HOST, exchange, symbol))
    if price_response.status_code != 200:
        print('could not get price for {}.{} : status {}'.format(
            exchange, symbol, price_response.status_code))
        return None
    print(price_response.json())
    return price_response.json()['price']


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


def save_price(exchange, symbol, price):
    s3_client = boto3.client('s3')
    KEY_NAME = 'prices.json'
    FILE_NAME = '/tmp/' + KEY_NAME

    price_data = {}
    try:
        s3_client.download_file(BUCKET_NAME, KEY_NAME, FILE_NAME)
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
        s3_client.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
    except ClientError as e:
        print(e)

    save_price_to_database(exchange, symbol, price)

    return price_data


def save_price_to_database(exchange, symbol, price):
    conn = get_database_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute('SELECT * FROM price WHERE exchange = %s AND symbol = %s;',
                [
                    exchange,
                    symbol
                ])
    rows = cur.fetchall()
    if len(rows) > 0:
        cur.execute('UPDATE price SET price = %s WHERE exchange = %s AND symbol = %s;',
                    [
                        price,
                        exchange,
                        symbol
                    ])
    else:
        cur.execute('INSERT INTO price (exchange, symbol, price) '
                    'VALUES (%s, %s, %s);',
                    [
                        exchange,
                        symbol,
                        price
                    ])
    conn.commit()


def save_price_history(exchange, symbol, date, price):

    s3_client = boto3.client('s3')
    KEY_NAME = 'price_history.json'
    FILE_NAME = '/tmp/' + KEY_NAME

    price_data = {}
    try:
        s3_client.download_file(BUCKET_NAME, KEY_NAME, FILE_NAME)
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
        s3_client.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
    except ClientError as e:
        print(e)

    save_price_history_to_database(exchange, symbol, date, price)

    return price_data


def save_price_history_to_database(exchange, symbol, date, price):
    conn = get_database_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute('DELETE FROM price_history WHERE exchange = %s AND symbol = %s AND date = %s',
                [
                    exchange,
                    symbol,
                    date
                ])
    cur.execute('INSERT INTO price_history (exchange, symbol, date, price) '
                'VALUES (%s, %s, %s, %s);',
                [
                    exchange,
                    symbol,
                    date,
                    price
                ])
    conn.commit()
