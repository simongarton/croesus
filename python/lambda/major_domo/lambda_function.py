import json
import requests
import datetime
import random
import time
import os
import psycopg2
import sys
import pytz


TIMEZONE = pytz.timezone('Pacific/Auckland')
HOST = "https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com"


# better error handling
# logs

def lambda_handler(event, context):
    todays_date = datetime.datetime.now(TIMEZONE).strftime("%Y-%m-%d")
    holdings_response = requests.get("{}/all_holdings?date={}".format(HOST, todays_date))
    print(holdings_response)
    if holdings_response.status_code != 200:
        return response(holdings_response.status_code, holdings_response.text)
    updates = 0
    for holding in holdings_response.json():
        exchange = holding["exchange"].upper()
        symbol = holding["symbol"].upper()
        update_price(exchange, symbol, todays_date)
        updates = updates + 1

    # also do exchange rate
    post_todays_exchange_rate("USD", "NZD")
    post_todays_exchange_rate("AUD", "NZD")

    # and rebuild value table
    rebuild_value_table()
    
    return response(200, {"message": "{} prices updated".format(updates)})


def post_todays_exchange_rate(source, target):
    url = "{}/exchange-rate/{}/{}".format(HOST, source, target)
    print("updating exchange rate : {}".format(url))
    requests.post(url)
    print("updated exchange rate.")


def rebuild_value_table():
    url = "{}/value".format(HOST)
    print("rebuilding value table : {}".format(url))
    requests.post(url)
    print("rebuilt value table.")


def update_price(exchange, symbol, date):
    url = "{}/stocks/{}/{}/{}".format(HOST, exchange, symbol, date)
    print(url)
    price_response = requests.post(url)
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
