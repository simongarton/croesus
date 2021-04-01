import json
import datetime
import dateparser
import psycopg2
import os


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
        print("could not get database connection")
        return None


def lambda_handler(event, context):
    # bug this is US time so doesn't work in the mornings; should add a day ?
    query_date = datetime.date.today()
    if "queryStringParameters" in event:
        if "date" in event["queryStringParameters"]:
            query_date = dateparser.parse(event["queryStringParameters"]["date"]).date()

    if not "pathParameters" in event:
        return response(400, {"error": "no path parameters, need account"})

    method = event["requestContext"]["http"]["method"]
    parameters = event["pathParameters"]

    if method == "GET":
        return get(parameters, query_date)
    return response(405, {"error": "unhandled method"})


def get(parameters, query_date):
    if "symbol" in parameters:
        return get_symbol_response(parameters, query_date)
    if "exchange" in parameters:
        return get_exchange_response(parameters, query_date)
    return get_total_response(parameters, query_date)


def get_total_response(parameters, query_date):
    account = parameters["account"]
    return response(200, get_holdings(account, None, None, query_date))


def get_exchange_response(parameters, query_date):
    exchange = parameters["exchange"]
    account = parameters["account"]
    return response(200, get_holdings(account, exchange, None, query_date))


def get_symbol_response(parameters, query_date):
    exchange = parameters["exchange"]
    symbol = parameters["symbol"]
    account = parameters["account"]
    return response(200, get_holdings(account, exchange, symbol, query_date))


# same code : value and holdings
def get_holdings(account, exchange, symbol, query_date):
    print("get")
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

    holdings_map = {}

    for transaction in transactions:
        print(transaction)
        transaction_date = transaction[1]
        if transaction_date > query_date:
            print('date')
            continue
        if exchange is not None:
            if transaction[2] != exchange:
                print('exchange')
                continue
        if symbol is not None:
            if transaction[3] != symbol:
                print('symbol')
                continue
        key = transaction[2] + ":" + transaction[3]
        if not key in holdings_map:
            holdings_map[key] = 0
        holdings_map[key] = holdings_map[key] + transaction[5]

    holdings = []
    for key, value in holdings_map.items():
        parts = key.split(":")
        exchange = parts[0]
        symbol = parts[1]
        holdings.append(
            {
                "exchange": exchange,
                "symbol": symbol,
                "quantity": round(value, 2),
            }
        )

    # sort
    holdings.sort(key=lambda x: x["exchange"] + ":" + x["symbol"])
    return holdings
