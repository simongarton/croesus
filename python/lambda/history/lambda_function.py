import os
import sys
import datetime
import json
from datetime import date
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
        return {
            "statusCode": 500,
            "body": json.dumps("connection error : {}".format(sys.exc_info()[0])),
        }


def lambda_handler(event, context):
    if not "pathParameters" in event:
        return response(400, {"error": "no parameters - need account"})
    parameters = event["pathParameters"]
    if not "account" in parameters:
        return response(400, {"error": "no parameters - need account"})

    account = parameters["account"]
    if not "exchange" in parameters:
        return response(200, get_total_history(account))
    if not "symbol" in parameters:
        exchange = parameters["exchange"]
        return response(200, get_exchange_history(account, exchange))
    exchange = parameters["exchange"]
    symbol = parameters["symbol"]
    return response(200, get_symbol_history(account, exchange, symbol))


def get_total_history(account):
    # here is the problem. If I don't get a value for a US stock on a day, then the total drops. I need to fix that value table at source.
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    sql = "SELECT date, sum(value)::numeric::float8 AS value FROM value GROUP BY date ORDER BY date;"
    params = []
    if account != "all":
        sql = "SELECT date, sum(value)::numeric::float8 AS value FROM value WHERE account = %s GROUP BY date ORDER BY date;"
        params = [account]
    cur.execute(sql, params)

    rows = cur.fetchall()
    data = []
    for row in rows:
        point = {"date": row[0], "value": row[1]}
        data.append(point)
    return data


def get_exchange_history(account, exchange):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    sql = """
        SELECT date, exchange, sum(value::numeric::float8) AS exchange_value
        FROM value 
        WHERE exchange = %s 
        GROUP BY date, exchange
        ORDER BY date, exchange;
        """
    params = [exchange]
    if account != "all":
        sql = """
        SELECT date, exchange, sum(value::numeric::float8) AS exchange_value
        FROM value 
        WHERE exchange = %s 
        AND account = %s
        GROUP BY date, exchange
        ORDER BY date, exchange;
        """
        params = [exchange, account]
    cur.execute(sql, params)

    rows = cur.fetchall()
    data = []
    for row in rows:
        point = {"date": row[0], "exchange": row[1], "value": row[2]}
        data.append(point)
    return data


def get_symbol_history(account, exchange, symbol):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    sql = """
        SELECT date, exchange, symbol, price::numeric::float8, quantity, value::numeric::float8
        FROM value 
        WHERE exchange = %s 
        AND symbol = %s 
        ORDER BY date, exchange, symbol;
        """
    params = [exchange, symbol]
    if account != "all":
        sql = """
        SELECT date, exchange, symbol, price::numeric::float8, quantity, value::numeric::float8
        FROM value 
        WHERE exchange = %s 
        AND symbol = %s 
        AND account = %s
        ORDER BY date, exchange, symbol;
        """
        params = [exchange, symbol, account]
    cur.execute(sql, params)

    rows = cur.fetchall()
    data = []
    for row in rows:
        point = {
            "date": row[0],
            "exchange": row[1],
            "symbol": row[2],
            "price": row[3],
            "quantity": round(row[4], 2),
            "value": row[5],
        }
        data.append(point)
    return data
