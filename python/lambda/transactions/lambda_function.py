import json
import os
import datetime
import psycopg2

# better error handling
# write to logs


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
    conn = get_database_connection()
    if not conn:
        return False
    cur = conn.cursor()
    cur.execute('INSERT INTO transaction (date, exchange, symbol, quantity, price) '
                'VALUES (%s, %s, %s, %s, %s);',
                [
                    date,
                    exchange,
                    symbol,
                    quantity,
                    price
                ])

    conn.commit()
    return True


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
    conn = get_database_connection()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute(
        'SELECT id, date, exchange, symbol, quantity, price FROM transaction ORDER BY date, exchange, symbol')

    transactions = cur.fetchall()

    if exchange is None:
        return transactions

    exchange_transactions = [
        t for t in transactions if t[2] == exchange]

    if symbol is None:
        return exchange_transactions

    symbol_transactions = [
        t for t in exchange_transactions if t[3] == symbol]
    return symbol_transactions


def test():
    print(get_transactions(None, None))


test()
