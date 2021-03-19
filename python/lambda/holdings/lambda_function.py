import json
import datetime
import dateparser
import psycopg2
import os

# better error handling
# write to logs


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
        method = event["requestContext"]["http"]["method"]
        if method == "GET":
            return get_total_response(query_date)
        return response(405, {"error": "unhandled method"})

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
    return get_total_response(query_date)


def get_total_response(query_date):
    return response(200, get_holdings(None, None, query_date))


def get_exchange_response(parameters, query_date):
    exchange = parameters["exchange"]
    return response(200, get_holdings(exchange, None, query_date))


def get_symbol_response(parameters, query_date):
    exchange = parameters["exchange"]
    symbol = parameters["symbol"]
    return response(200, get_holdings(exchange, symbol, query_date))


def get_holdings(exchange, symbol, query_date):
    conn = get_database_connection()
    if not conn:
        return []
    print(conn)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, date, exchange, symbol, quantity, price FROM transaction ORDER BY date, exchange, symbol"
    )

    transactions = cur.fetchall()

    holdings_map = {}

    print("{} {} {}".format(exchange, symbol, query_date))

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
        key = transaction[2] + ":" + transaction[3]
        if not key in holdings_map:
            holdings_map[key] = 0
        print("adding {}:{}".format(key, transaction[4]))
        holdings_map[key] = holdings_map[key] + transaction[4]

    holdings = []
    for key, value in holdings_map.items():
        parts = key.split(":")
        exchange = parts[0]
        symbol = parts[1]
        holdings.append({"exchange": exchange, "symbol": symbol, "quantity": value})

    # sort
    holdings.sort(key=lambda x: x["exchange"] + ":" + x["symbol"])
    return holdings
