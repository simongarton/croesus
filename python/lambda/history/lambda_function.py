

import os
import sys
import datetime
import json
from datetime import date
import psycopg2

HOST = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com'


def response(code, body):
    return {
        'statusCode': code,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(body, default=date_converter)
    }


def date_converter(o):
    if isinstance(o, datetime.datetime):
        return o.strftime('%Y-%m-%d')
    if isinstance(o, datetime.date):
        return o.strftime('%Y-%m-%d')
    return '{}'.format(o)


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
        return response(200, get_total_history())
    parameters = event['pathParameters']
    if not 'symbol' in parameters:
        exchange = parameters['exchange']
        return response(200, get_exchange_history(exchange))
    exchange = parameters['exchange']
    symbol = parameters['symbol']
    return response(200, get_symbol_history(exchange, symbol))


def get_total_history():
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute(
        'SELECT date, sum(value::numeric::float8) AS total_value FROM value GROUP BY date ORDER BY date;')
    return cur.fetchall()


def get_exchange_history(exchange):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute('''
        SELECT date, exchange, sum(value::numeric::float8) AS exchange_value
        FROM value 
        WHERE exchange = %s 
        GROUP BY date, exchange
        ORDER BY date, exchange;
        ''',
                [
                    exchange,
                ])
    return cur.fetchall()


def get_symbol_history(exchange, symbol):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute('''
        SELECT date, exchange, symbol, price::numeric::float8, quantity, value::numeric::float8 
        FROM value 
        WHERE exchange = %s AND symbol = %s
        ORDER BY date, exchange, symbol;
        ''',
                [
                    exchange,
                    symbol
                ])
    return cur.fetchall()
