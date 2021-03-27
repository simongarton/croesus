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

    if not "pathParameters" in event:
        return response(400, {"error": "no parameters - need account"})

    method = event["requestContext"]["http"]["method"]
    parameters = event["pathParameters"]

    if not "account" in parameters:
        return response(400, {"error": "no parameters - need account"})

    if method == "GET":
        return get(parameters)
    if method == "POST":
        return post(parameters, json.loads(event["body"]))
    return response(405, {"error": "unhandled method"})


def get(parameters):
    if "symbol" in parameters:
        return get_symbol_response(parameters)
    if "exchange" in parameters:
        return get_exchange_response(parameters)
    return get_total_response(parameters)


def post(parameters, body):
    if "symbol" in parameters:
        return post_symbol(parameters, body)


def post_symbol(parameters, body):
    exchange = parameters["exchange"]
    symbol = parameters["symbol"]
    account = parameters["account"]
    date = body["date"]
    quantity = body["quantity"]
    price = body["price"]
    return response(
        200, add_transaction(exchange, symbol, account, date, quantity, price)
    )


def add_transaction(exchange, symbol, account, date, quantity, price):
    conn = get_database_connection()
    if not conn:
        return False
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transaction (date, exchange, symbol, account, quantity, price) "
        "VALUES (%s, %s, %s, %s, %s);",
        [date, exchange, symbol, account, quantity, price],
    )

    conn.commit()
    return True


def get_total_response(parameters):
    account = parameters["account"]
    return response(200, get_transactions(account, None, None))


def get_exchange_response(parameters):
    account = parameters["account"]
    exchange = parameters["exchange"]
    return response(200, get_transactions(account, exchange, None))


def get_symbol_response(parameters):
    account = parameters["account"]
    exchange = parameters["exchange"]
    symbol = parameters["symbol"]

    return response(200, get_transactions(account, exchange, symbol))


def map_transaction(row):
    return {
        "id": row[0],
        "date": row[1],
        "exchange": row[2],
        "symbol": row[3],
        "account": row[4],
        "quantity": row[5],
        "price": row[6],
    }


def get_transactions(account, exchange, symbol):
    conn = get_database_connection()
    if not conn:
        return []
    cur = conn.cursor()
    sql = "SELECT id, date, exchange, symbol, account, quantity, price FROM transaction ORDER BY date, exchange, symbol"
    params = []
    if account != "all":
        sql = "SELECT id, date, exchange, symbol, account, quantity, price FROM transaction WHERE account = %s ORDER BY date, exchange, symbol"
        params = [account]

    cur.execute(sql, params)

    transactions = cur.fetchall()

    if exchange is None:
        all_transactions = [map_transaction(t) for t in transactions]
        return all_transactions

    exchange_transactions = [t for t in transactions if t[2] == exchange]

    if symbol is None:
        return [map_transaction(t) for t in exchange_transactions]

    symbol_transactions = [
        map_transaction(t) for t in exchange_transactions if t[3] == symbol
    ]
    return symbol_transactions