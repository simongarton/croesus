import json
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

    # I have to do the current day's holdings as I only can get new prices for the current day

    todays_date = datetime.datetime.now().strftime('%Y-%m-%d')
    print("getting holdings for {}".format(todays_date))
    holdings_response = requests.get(
        '{}/holdings?date={}'.format(HOST, todays_date))
    if holdings_response.status_code != 200:
        print(holdings_response)
        return response(holdings_response.status_code, holdings_response.text)
    print(holdings_response)
    updates = 0
    for holding in holdings_response.json():
        exchange = holding['exchange']
        symbol = holding['symbol']
        price = get_price(exchange, symbol)
        if not price:
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

    save_price_to_database(exchange, symbol, price)

    return get_price_data_from_database()


def get_price_data_from_database():
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute('SELECT * FROM price ORDER BY exchange, symbol')
    rows = cur.fetchall()
    return rows


def get_price_history_data_from_database():
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM price_history ORDER BY date DESC, exchange, symbol')
    rows = cur.fetchall()
    return rows


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

    save_price_history_to_database(exchange, symbol, date, price)

    return get_price_history_data_from_database()


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
