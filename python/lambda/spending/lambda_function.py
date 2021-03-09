import json
import os
import datetime
import psycopg2

# better error handling
# logs


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
        print("could not get database connection")
        return None


def lambda_handler(event, context):

    if 'pathParameters' in event:
        parameters = event['pathParameters']
        filter_exchange = parameters['exchange'] if 'exchange' in parameters else None
        filter_symbol = parameters['symbol'] if 'symbol' in parameters else None
        print("got {} and {}".format(filter_exchange, filter_symbol))
    else:
        filter_exchange = None
        filter_symbol = None

    return handle(filter_exchange, filter_symbol)


def handle(filter_exchange, filter_symbol):
    if filter_exchange == None:
        return response(200, get_total_spending())
    if filter_symbol == None:
        return response(200, get_exchange_spending(filter_exchange))
    return response(200, get_symbol_spending(filter_exchange, filter_symbol))


def get_total_spending():
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute('''
        SELECT date, sum(price * quantity)::numeric::float8 AS total
        FROM transaction
        GROUP BY date
        ORDER BY date;
        ''',
                [
                ])
    rows = cur.fetchall()
    data = []
    for row in rows:
        point = {
            'date': row[0],
            'total': round(row[1], 2)
        }
        data.append(point)
    return data


def get_exchange_spending(filter_exchange):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute('''
        SELECT date, exchange, sum(price * quantity)::numeric::float8 AS total
        FROM transaction
        WHERE exchange = %s 
        GROUP BY date, exchange
        ORDER BY date, exchange;
        ''',
                [
                    filter_exchange
                ])
    rows = cur.fetchall()
    data = []
    for row in rows:
        point = {
            'date': row[0],
            'exchange': row[1],
            'total': round(row[2], 2)
        }
        data.append(point)
    return data


def get_symbol_spending(filter_exchange, filter_symbol):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute('''
        SELECT date, exchange, symbol, sum(price * quantity)::numeric::float8 AS total
        FROM transaction
        WHERE exchange = %s AND symbol = %s
        GROUP BY date, exchange, symbol
        ORDER BY date, exchange, symbol;
        ''',
                [
                    filter_exchange,
                    filter_symbol
                ])
    rows = cur.fetchall()
    data = []
    for row in rows:
        point = {
            'date': row[0],
            'exchange': row[1],
            'symbol': row[2],
            'total': round(row[3], 2)
        }
        data.append(point)
    return data
