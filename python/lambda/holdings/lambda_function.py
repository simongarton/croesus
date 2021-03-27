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
    query_date = datetime.date.today()
    print("defaulted query date as {}".format(query_date))
    if "queryStringParameters" in event:
        if "date" in event["queryStringParameters"]:
            query_date = dateparser.parse(event["queryStringParameters"]["date"]).date()
            print("parsed query date as {}".format(query_date))

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


def get_holdings(account, exchange, symbol, query_date):
    conn = get_database_connection()
    if not conn:
        return []
    print(conn)
    cur = conn.cursor()
    sql = "SELECT id, date, exchange, symbol, account, quantity, price FROM transaction ORDER BY date, exchange, symbol"
    params = []
    if account != "all":
        sql = "SELECT id, date, exchange, symbol, account, quantity, price FROM transaction WHERE account = %s ORDER BY date, exchange, symbol"
        params = [account]
    cur.execute(sql, params)

    transactions = cur.fetchall()

    holdings_map = {}

    print("{} {} {} {}".format(exchange, symbol, account, query_date))

    for transaction in transactions:
        print(transaction)
        transaction_date = transaction[1]
        print("{}={}".format(transaction_date, query_date))
        if transaction_date > query_date:
            print("out of date range {} > {}".format(transaction_date, query_date))
            continue
        if exchange is not None:
            if transaction[2] != exchange:
                print("failed exchange {} != {}".format(transaction[2], exchange))
                continue
        if symbol is not None:
            if transaction[3] != symbol:
                print("failed symbol {} != {}".format(transaction[3], symbol))
                continue
        key = transaction[2] + ":" + transaction[3] + ":" + transaction[4]
        if not key in holdings_map:
            holdings_map[key] = 0
        print("adding {}:{}".format(key, transaction[5]))
        holdings_map[key] = holdings_map[key] + transaction[5]

    holdings = []
    for key, value in holdings_map.items():
        parts = key.split(":")
        exchange = parts[0]
        symbol = parts[1]
        account = parts[2]
        holdings.append(
            {
                "exchange": exchange,
                "symbol": symbol,
                "account": account,
                "quantity": value,
            }
        )

    # sort
    holdings.sort(key=lambda x: x["exchange"] + ":" + x["symbol"])
    return holdings
