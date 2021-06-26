import json
import os
import datetime
import psycopg2


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=date_converter),
    }


def date_converter(o):
    if isinstance(o, datetime.datetime):
        return o.strftime("%Y-%m-%d")
    if isinstance(o, datetime.date):
        return o.strftime("%Y-%m-%d")
    return "{}".format(o)


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
        print("could not get database connection")
        return None


def lambda_handler(event, context):

    method = event["requestContext"]["http"]["method"]
    parameters = event["pathParameters"] if "pathParameters" in event else {}

    if method == "GET":
        return get(parameters)
    return response(405, {"error": "unhandled method"})


def get(parameters):
    account = parameters["account"] if "account" in parameters else None
    exchange = parameters["exchange"] if "exchange" in parameters else None
    symbol = parameters["symbol"] if "symbol" in parameters else None
    return response(200, get_transactions(account, exchange, symbol))


def map_transaction(row, prices):
    print(row)
    key = row[2] + ':' + row[3]
    current_price = prices[key]
    print('{} {}'.format(key, current_price))
    current_value = round(row[5] * current_price,2)
    purchase_value = round(row[5] * row[6], 2)
    gain_loss = round(current_value - purchase_value, 2)
    gain_loss_percentage = round(gain_loss/purchase_value, 4)
    days = (datetime.date.today() - row[1]).days
    years = days/365
    cagr = round(pow((current_value/purchase_value),(1/years)) - 1, 4)
    return {
        "id": row[0],
        "date": row[1],
        "exchange": row[2],
        "symbol": row[3],
        "account": row[4],
        "quantity": row[5],
        "purchase_price": row[6],
        "purchase_value": purchase_value,
        "current_price": current_price,
        "current_value": current_value,
        "overall_gain_loss": gain_loss,
        "overall_gain_loss_percentage": gain_loss_percentage,
        "annual_gain_loss": round(gain_loss/years, 2),
        "annual_gain_loss_percentage": cagr,
    }

def get_prices(conn):
    cur = conn.cursor()
    sql = "SELECT exchange, symbol, price::numeric::float8 FROM price ORDER BY exchange, symbol"
    cur.execute(sql)

    rows = cur.fetchall()
    prices = {}
    for row in rows:
        key = row[0] + ':' + row[1]
        value = row[2]
        prices[key] = value

    return prices 


def get_transactions(account, exchange, symbol):
    conn = get_database_connection()
    if not conn:
        return []
    prices = get_prices(conn)
    cur = conn.cursor()
    sql = "SELECT id, date, exchange, symbol, account, quantity, price::numeric::float8 FROM transaction ORDER BY date, exchange, symbol"
    params = []
    if account:
        sql = "SELECT id, date, exchange, symbol, account, quantity, price::numeric::float8 FROM transaction WHERE account = %s ORDER BY date, exchange, symbol"
        params = [account]

    cur.execute(sql, params)

    transactions = cur.fetchall()

    if exchange is None:
        all_transactions = [map_transaction(t, prices) for t in transactions]
        return all_transactions

    exchange_transactions = [t for t in transactions if t[2] == exchange]

    if symbol is None:
        return [map_transaction(t, prices) for t in exchange_transactions]

    symbol_transactions = [
        map_transaction(t, prices) for t in exchange_transactions if t[3] == symbol
    ]
    return symbol_transactions