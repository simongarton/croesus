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
    parameters = event["pathParameters"] if "pathParameters" in event else {}
    account = parameters["account"] if "account" in parameters else None
    exchange = parameters["exchange"] if "exchange" in parameters else None
    symbol = parameters["symbol"] if "symbol" in parameters else None

    if not exchange:
        return response(200, get_total_spending(account))
    if not symbol:
        exchange = parameters["exchange"]
        return response(200, get_exchange_spending(account, exchange))
    return response(200, get_symbol_spending(account, exchange, symbol))


def get_total_spending(account):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    sql = """
        SELECT date, sum(price * quantity)::numeric::float8 AS total
        FROM transaction
        GROUP BY date
        ORDER BY date;
        """
    params = []
    if account:
        sql = """
        SELECT date, sum(price * quantity)::numeric::float8 AS total
        FROM transaction
        WHERE account = %s 
        GROUP BY date
        ORDER BY date;
        """
        params = [account]
    cur.execute(sql, params)

    rows = cur.fetchall()
    total = 0
    data = []
    for row in rows:
        point = {"date": row[0], "total": round(row[1], 2)}
        data.append(point)
        total = total + row[1]
    return {"total": round(total, 2), "spending": data}


def get_exchange_spending(account, filter_exchange):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    sql = """
        SELECT date, exchange, sum(price * quantity)::numeric::float8 AS total
        FROM transaction
        WHERE exchange = %s 
        GROUP BY date, exchange
        ORDER BY date, exchange;
        """
    params = [filter_exchange]
    if account:
        sql = """
        SELECT date, exchange, sum(price * quantity)::numeric::float8 AS total
        FROM transaction
        WHERE exchange = %s 
        AND account = %s 
        GROUP BY date, exchange
        ORDER BY date, exchange;
        """
        params = [filter_exchange, account]
    cur.execute(sql, params)

    rows = cur.fetchall()
    total = 0
    data = []
    for row in rows:
        point = {"date": row[0], "exchange": row[1], "total": round(row[2], 2)}
        data.append(point)
        total = total + row[2]
    return {"total": round(total, 2), "spending": data}


def get_symbol_spending(account, filter_exchange, filter_symbol):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    sql = """
        SELECT date, exchange, symbol, sum(price * quantity)::numeric::float8 AS total
        FROM transaction
        WHERE exchange = %s AND symbol = %s
        GROUP BY date, exchange, symbol
        ORDER BY date, exchange, symbol;
        """
    params = [filter_exchange, filter_symbol]
    if account:
        sql = """
        SELECT date, exchange, symbol, sum(price * quantity)::numeric::float8 AS total
        FROM transaction
        WHERE exchange = %s AND symbol = %s AND account = %s
        GROUP BY date, exchange, symbol
        ORDER BY date, exchange, symbol;
        """
        params = [filter_exchange, filter_symbol, account]
    cur.execute(sql, params)

    rows = cur.fetchall()
    total = 0
    data = []
    for row in rows:
        point = {
            "date": row[0],
            "exchange": row[1],
            "symbol": row[2],
            "total": round(row[3], 2),
        }
        data.append(point)
        total = total + row[3]
    return {"total": round(total, 2), "spending": data}
