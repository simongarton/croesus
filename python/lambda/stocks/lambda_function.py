import os
import requests
import json
from datetime import date, datetime, timedelta
import psycopg2
import sys
import pytz
import yfinance as yf


TIMEZONE = pytz.timezone('Pacific/Auckland')
HOST = "https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com"
API_KEY = "5tl4ks_0QZJP5J8pE6JdvDbeXuQ7Cm1f"

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
    if not "pathParameters" in event:
        return {"statusCode": 400, "body": {"message": "no pathParameters"}}
    parameters = event["pathParameters"]
    for param in ["symbol", "exchange"]:
        if not param in parameters:
            return {
                "statusCode": 400,
                "body": {"message": "no {} in parameters".format(param)},
            }
    exchange = parameters["exchange"].upper()
    symbol = parameters["symbol"].upper()
    if not "date" in parameters:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        date = parameters["date"]
    method = event["requestContext"]["http"]["method"]

    if method == "POST":
        return post_stock(exchange, symbol, date)
    return get_stock(exchange, symbol, date)


def get_generic_stock(exchange, suffix, currency, symbol, date):
    return generic_stock(exchange, suffix, currency, symbol, date, False)


def post_generic_stock(exchange, suffix, currency, symbol, date):
    return generic_stock(exchange, suffix, currency, symbol, date, True)


def generic_stock(exchange, suffix, currency, symbol, date, save):
    actual_date = datetime.strptime(date, "%Y-%m-%d")
    date = actual_date.strftime("%Y-%m-%d")
    print("{}.{} with suffix {} currency {} for date {}".format(exchange,symbol,suffix, currency,date))
    ticker = yf.Ticker(symbol + suffix) if suffix else yf.Ticker(symbol)
    data = ticker.info
    exchange_rate = get_exchange_rate(currency, date)
    if exchange_rate == None:
        return response(500, {"message": "no exchange rate for " + date})
    if not 'regularMarketPrice' in data :
        return response(404, {"exchange": exchange, "symbol": symbol})
    raw = data['regularMarketPrice']
    price = round(raw * exchange_rate, 3)
    print("{}.{} with suffix {} currency {} for date {} raw {} rate {} exchanged ".format(exchange,symbol,suffix, currency,date, raw, exchange_rate, price))
    
    if save:
        save_price_to_database(exchange, symbol, price)
        save_price_history_to_database(exchange, symbol, datetime.now(TIMEZONE).date(), price)

    return response(
        200,
        {
            "exchange": exchange,
            "symbol": symbol,
            "date": datetime.now(TIMEZONE).strftime("%Y-%m-%d"),
            "raw": raw,
            "exchange_rate": exchange_rate,
            "price": price,
        },
    )


def get_exchange_rate(currency, date):
    if not currency:
        return 1.0
    url = "{}/exchange-rate/{}/NZD/{}".format(HOST, currency, date)
    api_response = requests.get(url)
    api_response.raise_for_status()
    return api_response.json()["rate"]


def post_stock(exchange, symbol, date):
    if exchange == "ASX":
        return post_generic_stock(exchange, '.AX', 'AUD', symbol, date)
    if exchange == "NZX":
        return post_generic_stock(exchange, '.NZ', None, symbol, date)
    if exchange == "NYSE":
        return post_generic_stock(exchange, None, 'USD', symbol, date)
    if exchange == "NASDAQ":
        return post_generic_stock(exchange, None, 'USD', symbol, date)
    if exchange == "CBOE":
        return post_generic_stock(exchange, None, 'USD', symbol, date)
    return response(400, "invalid exchange " + exchange)


def get_stock_live(exchange, symbol, date):
    if exchange == "ASX":
        return get_generic_stock(exchange, '.AX', 'AUD', symbol, date)
    if exchange == "NZX":
        return get_generic_stock(exchange, '.NZ', None, symbol, date)
    if exchange == "NYSE":
        return get_generic_stock(exchange, None, 'USD', symbol, date)
    if exchange == "NASDAQ":
        return get_generic_stock(exchange, None, 'USD', symbol, date)
    if exchange == "CBOE":
        return get_generic_stock(exchange, None, 'USD', symbol, date)
    return response(400, "invalid exchange " + exchange)


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


def save_price_to_database(exchange, symbol, price):
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


def save_price_history_to_database(exchange, symbol, date, price):
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