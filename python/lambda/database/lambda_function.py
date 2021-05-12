import os
import json
from datetime import date, datetime, timedelta
import psycopg2
import sys


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def get_database_connection():
    try:
        dbname = os.environ.get("PGDATABASE")
        user = os.environ.get("PGUSER")
        host = os.environ.get("PGHOST")
        password = os.environ.get("PGPASSWORD")
        connection = "dbname='{}' user='{}' host='{}' password='{}'".format(
            dbname, user, host, password
        )
        conn = psycopg2.connect(connection)
        return conn
    except:
        return response(500, "connection error : {}".format(sys.exc_info()[0]))


def lambda_handler(event, context):
    try:
        lambda_name = event['lambda']
        if lambda_name == 'exchange_rate':
            return handle_exchange_rate(event)
        if lambda_name == 'stocks':
            return handle_stocks(event)
        if lambda_name == 'croesus':
            return handle_croesus(event)
        return response(400, 'unable to handle database event for lambda \'{}\''.format(lambda_name))
    except Exception as e:
        return response(500, "failure in handler : {}".format(str(e)))


def handle_exchange_rate(event):
    lambda_name = event['lambda']
    method = event['method']
    if method == 'save_rate_to_database':
        return exchange_rate_save_rate_to_database(event)
    if method == 'get_rate':
        return exchange_rate_get_rate(event)
    return response(400, 'unable to handle database method {} for lambda \'{}\''.format(method, lambda_name))


def handle_stocks(event):
    lambda_name = event['lambda']
    method = event['method']
    if method == 'save_price_to_database':
        return stocks_save_price_to_database(event)
    if method == 'save_price_history_to_database':
        return stocks_save_price_history_to_database(event)
    return response(400, 'unable to handle database method {} for lambda \'{}\''.format(method, lambda_name))


def handle_croesus(event):
    lambda_name = event['lambda']
    method = event['method']
    if method == 'password':
        return croesus_password(event)
    return response(400, 'unable to handle database method {} for lambda \'{}\''.format(method, lambda_name))


def get_stock(exchange, symbol, date):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute(
        "SELECT id, exchange, symbol, price::numeric::float8 FROM price_history WHERE exchange = %s AND symbol = %s AND date = %s",
        [exchange, symbol, date],
    )
    rows = cur.fetchall()
    if len(rows) == 0:
        return response(404, {"exchange": exchange, "symbol": symbol, "date": date})
    return response(
        200, {"exchange": exchange, "symbol": symbol, "date": date, "price": rows[0][3]}
    )

def croesus_password(event):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute(
        "SELECT password FROM password WHERE password = %s ",
        [event['data']['password']],
    )
    rows = cur.fetchall()
    if len(rows) == 0:
        return response(401, {
            "outcome": "unauthorized",
            "code":401
            }
        )
    return response(200, {
            "outcome": "ok",
            "code":200
            }
        )

def stocks_save_price_to_database(event):
    data = event['data']
    exchange = data['exchange']
    symbol = data['symbol']
    price = data['price']
    return save_price_to_database(exchange, symbol, price)


def save_price_to_database(exchange, symbol, price):
    print("save_price_to_database : {}.{} @ {}".format(exchange, symbol, price))
    conn = get_database_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM price WHERE exchange = %s AND symbol = %s;", [exchange, symbol]
    )
    rows = cur.fetchall()
    if len(rows) > 0:
        cur.execute(
            "UPDATE price SET price = %s WHERE exchange = %s AND symbol = %s;",
            [price, exchange, symbol],
        )
    else:
        cur.execute(
            "INSERT INTO price (exchange, symbol, price) VALUES (%s, %s, %s);",
            [exchange, symbol, price],
        )
    conn.commit()
    print("save_price_to_database done")
    return response(
        200, {"exchange": exchange, "symbol": symbol, "price": price}
    )


def stocks_save_price_history_to_database(event):
    data = event['data']
    exchange = data['exchange']
    symbol = data['symbol']
    date = data['date']
    price = data['price']
    return save_price_history_to_database(exchange, symbol, date, price)

    
def save_price_history_to_database(exchange, symbol, date, price):
    print("save_price_history_to_database : {}.{} @ {} on {}".format(exchange, symbol, price, date))
    conn = get_database_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM price_history WHERE exchange = %s AND symbol = %s AND date = %s;",
        [exchange, symbol, date],
    )
    rows = cur.fetchall()
    if len(rows) > 0:
        cur.execute(
            "UPDATE price_history SET price = %s WHERE exchange = %s AND symbol = %s AND date = %s;",
            [price, exchange, symbol, date],
        )
    else:
        cur.execute(
            "INSERT INTO price_history (exchange, symbol, date, price) "
            "VALUES (%s, %s, %s, %s);",
            [exchange, symbol, date, price],
        )
    conn.commit()
    print("save_price_history_to_database done")
    return response(
        200, {"exchange": exchange, "symbol": symbol, "date": date, "price": price}
    )



def exchange_rate_save_rate_to_database(event):
    data = event['data']
    source = data['source']
    target = data['target']
    date = data['date']
    rate = data['rate']
    save_rate_to_database(source, target, date, rate)
    return response(200, event)


def save_rate_to_database(source, target, date, rate):
        conn = get_database_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute(
            'SELECT id FROM "exchange-rate" WHERE source = %s AND target = %s AND date = %s;',
            [source, target, date],
        )
        rows = cur.fetchall()
        if len(rows) > 0:
            cur.execute(
                'UPDATE "exchange-rate" SET rate = %s WHERE source = %s AND target = %s AND date = %s;',
                [rate, source, target, date],
            )
        else:
            cur.execute(
                'INSERT INTO "exchange-rate" (source, target, date, rate) VALUES (%s, %s, %s, %s);',
                [source, target, date, rate],
            )
        conn.commit()


def exchange_rate_get_rate(event):
    data = event['data']
    source = data['source']
    target = data['target']
    date = data['date']
    return get_rate(source, target, date)


def get_rate(source, target, date):
    conn = get_database_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute(
        'SELECT rate FROM "exchange-rate" WHERE source = %s AND target = %s AND date = %s;',
        [source, target, date],
    )
    rows = cur.fetchall()
    if len(rows) > 0:
        return response(
            200,
            {"source": source, "target": target, "date": date, "rate": rows[0][0]},
        )
    cur.execute(
        'SELECT rate FROM "exchange-rate" WHERE target = %s AND source = %s AND date = %s;',
        [source, target, date],
    )
    rows = cur.fetchall()
    if len(rows) > 0:
        return response(
            200,
            {
                "source": source,
                "target": target,
                "date": date,
                "rate": round(1 / rows[0][0], 3),
            },
        )
    return response(
        404, "{} not found with source {} on {}".format(target, source, date)
    )