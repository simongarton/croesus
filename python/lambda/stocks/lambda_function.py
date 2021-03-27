from typing import Text
from bs4 import BeautifulSoup
import os
import requests
import json
from datetime import date, datetime, timedelta
import psycopg2
import sys

HOST = "https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com"
API_KEY = "5tl4ks_0QZJP5J8pE6JdvDbeXuQ7Cm1f"

# GET calls will always go cached.
# POST calls will create the current and the historical record
# both will accept a date as the mandatory third parameter : /exchange/symbol/date
# though I will have to throw a 400 for NZX POST. POST will return it as well.
# I am removing cached


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
        return get_most_recent_value(exchange, symbol)
    date = parameters["date"]
    method = event["requestContext"]["http"]["method"]

    if method == "POST":
        return post_stock(exchange, symbol, date)
    return get_stock(exchange, symbol, date)


def get_most_recent_value(exchange, symbol):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute(
        "SELECT id, exchange, symbol, price::numeric::float8 FROM price WHERE exchange = %s AND symbol = %s",
        [exchange, symbol],
    )
    rows = cur.fetchall()
    if len(rows) == 0:
        return response(404, "not found")

    return response(200, {"exchange": exchange, "symbol": symbol, "price": rows[0][3]})


def getRandomUserAgent():
    uastrings = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",
    ]


def post_nzx_stock(symbol):
    exchange = "NZX"
    headers = {"User-Agent": getRandomUserAgent()}
    page = requests.get(
        "https://www.nzx.com/instruments/{}/".format(symbol), headers=headers
    )
    soup = BeautifulSoup(page.content, "html.parser")
    h1 = soup.find_all("h1")
    price = float(h1[1].text.strip().replace("$", ""))
    save_price_to_database(exchange, symbol, price)
    save_price_history_to_database(exchange, symbol, datetime.now().date(), price)
    return response(
        200,
        {
            "exchange": exchange,
            "symbol": symbol,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "price": price,
        },
    )


def get_exchange_rate(date):
    url = "{}/exchange-rate/USD/NZD/{}".format(HOST, date)
    api_response = requests.get(url)
    api_response.raise_for_status()
    return api_response.json()["rate"]


def post_nyse_stock(symbol, date):
    exchange = "NYSE"
    actual_date = datetime.strptime(date, "%Y-%m-%d")
    date = actual_date.strftime("%Y-%m-%d")
    url = "https://api.polygon.io/v1/open-close/{}/{}?apiKey={}".format(
        symbol, date, API_KEY
    )
    api_response = requests.get(url)
    api_response.raise_for_status()
    exchange_rate = get_exchange_rate(date)
    if exchange_rate == None:
        return response(500, {"message": "no exchange rate for " + date})
    price = round(api_response.json()["close"] * exchange_rate, 2)
    save_price_to_database(exchange, symbol, price)
    save_price_history_to_database(exchange, symbol, actual_date, price)
    # temp
    save_value_to_database(exchange, symbol, actual_date, price)
    return response(
        200,
        {
            "exchange": exchange,
            "symbol": symbol,
            "date": date,
            "price": price,
        },
    )


def post_stock(exchange, symbol, date):
    if exchange == "NZX":
        return post_nzx_stock(symbol)
    if exchange == "NYSE":
        return post_nyse_stock(symbol, date)
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
        return response(404, "not found")
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


def save_value_to_database(exchange, symbol, date, price):
    holdings_response = requests.get(
        "{}/holdings/{}/{}?date={}".format(HOST, exchange, symbol, date)
    )
    holdings_response.raise_for_status()
    quantity = 0
    for holding in holdings_response.json():
        quantity = quantity = holding["quantity"]
    value = quantity * price

    conn = get_database_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM value WHERE exchange = %s AND symbol = %s AND date = %s;",
        [exchange, symbol, date],
    )
    rows = cur.fetchall()
    if len(rows) > 0:
        cur.execute(
            "UPDATE value SET price = %s, quantity = %s, value = %s WHERE exchange = %s AND symbol = %s AND date = %s;",
            [price, quantity, value, exchange, symbol, date],
        )
    else:
        cur.execute(
            "INSERT INTO value (exchange, symbol, date, price, quantity, value) "
            "VALUES (%s, %s, %s, %s, %s, %s);",
            [exchange, symbol, date, price, quantity, value],
        )
    conn.commit()
