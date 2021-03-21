import json
import requests
import datetime
import random
import time
import os
import psycopg2
import sys


HOST = "https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com"


# better error handling
# logs


def lambda_handler(event, context):

    todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
    older_date = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime(
        "%Y-%m-%d"
    )
    # bug where's older_date in this ? compare to older price used later
    print("getting holdings for {}".format(todays_date))
    holdings_response = requests.get("{}/holdings?date={}".format(HOST, todays_date))
    if holdings_response.status_code != 200:
        print(holdings_response)
        return response(holdings_response.status_code, holdings_response.text)
    total_value = 0
    updates = 0
    for holding in holdings_response.json():
        exchange = holding["exchange"].upper()
        symbol = holding["symbol"].upper()
        quantity = holding["quantity"]
        price = get_price(
            exchange, symbol, older_date if exchange == "NYSE" else todays_date
        )
        if not price:
            continue
        print("saving {} of {}.{} at {}".format(quantity, exchange, symbol, price))
        value = quantity * price
        total_value = total_value + value
        print("value {} total_value {}".format(value, total_value))
        save_value(exchange, symbol, todays_date, price, quantity, value)
        updates = updates + 1
        time.sleep(random.randint(0, 20) / 10.0)

    save_total_value(todays_date, total_value)
    return response(200, {"message": "{} prices updated".format(updates)})


def get_price(exchange, symbol, todays_date):
    # first we get it from the cache
    url = "{}/stocks/{}/{}/{}".format(HOST, exchange, symbol, todays_date)
    print("getting {}".format(url))
    price_response = requests.get(url)
    # if not found, try POSTing to refresh it
    if price_response.status_code == 404:
        print("posting {}".format(url))
        price_response = requests.post(url)
        print("getting again {}".format(url))
        price_response = requests.get(url)
    if price_response.status_code != 200:
        print(
            "could not get price for {}.{} : status {}".format(
                exchange, symbol, price_response.status_code
            )
        )
        return None
    print(price_response.json())
    return price_response.json()["price"]


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
        return {
            "statusCode": 500,
            "body": json.dumps("connection error : {}".format(sys.exc_info()[0])),
        }


def save_price(exchange, symbol, price):

    save_price_to_database(exchange, symbol, price)

    return get_price_data_from_database()


def get_price_data_from_database():
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute(
        "SELECT id, exchange, symbol, price FROM price ORDER BY exchange, symbol"
    )
    rows = cur.fetchall()
    return rows


def get_price_history_data_from_database():
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute(
        "SELECT id, date, exchange, symbol, price FROM price_history ORDER BY date DESC, exchange, symbol"
    )
    rows = cur.fetchall()
    return rows


def get_value_data_from_database():
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute(
        "SELECT id, date, exchange, symbol, price, quantity, value FROM value ORDER BY date DESC, exchange, symbol"
    )
    rows = cur.fetchall()
    return rows


def get_total_value_data_from_database():
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute("SELECT id, date, value FROM total_value ORDER BY date DESC")
    rows = cur.fetchall()
    return rows


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
            "INSERT INTO price (exchange, symbol, price) " "VALUES (%s, %s, %s);",
            [exchange, symbol, price],
        )
    conn.commit()


def save_price_history(exchange, symbol, date, price):
    save_price_history_to_database(exchange, symbol, date, price)

    return get_price_history_data_from_database()


def save_value(exchange, symbol, date, price, quantity, value):
    save_value_to_database(exchange, symbol, date, price, quantity, value)

    return get_value_data_from_database()


def save_total_value(date, total_value):
    save_total_value_to_database(date, total_value)

    return get_total_value_data_from_database()


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


def save_value_to_database(exchange, symbol, date, price, quantity, value):
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


def save_total_value_to_database(date, value):
    conn = get_database_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("SELECT id FROM total_value WHERE date = %s;", [date])
    rows = cur.fetchall()
    if len(rows) > 0:
        cur.execute("UPDATE total_value SET value = %s WHERE date = %s;", [value, date])
    else:
        cur.execute(
            "INSERT INTO total_value (date, value) " "VALUES (%s, %s);", [date, value]
        )
    conn.commit()
