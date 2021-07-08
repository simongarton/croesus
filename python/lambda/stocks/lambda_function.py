import os
import requests
import json
from datetime import date, datetime, timedelta
import sys
import pytz
import yfinance as yf
import boto3
import numpy as np


TIMEZONE = pytz.timezone('Pacific/Auckland')
HOST = "https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com"
API_KEY = "5tl4ks_0QZJP5J8pE6JdvDbeXuQ7Cm1f"
lambda_client = boto3.client('lambda')


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    if 'update_prices' in event['rawPath']:
        update_prices_for_date(event)
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
    previous_day = actual_date - timedelta(days=1)
    date = actual_date.strftime("%Y-%m-%d")
    previous_date = previous_day.strftime("%Y-%m-%d")
    exchange_rate = get_exchange_rate(currency, date)
    print(exchange_rate)
    if exchange_rate == None:
        return response(500, {"message": "no exchange rate for {} on {}".format(currency, date)})

    print("exchange {} symbol {} with suffix {} currency {} for date {} actual_date ".format(exchange, symbol, suffix, currency, date, actual_date))
    ticker = yf.Ticker(symbol + suffix) if suffix else yf.Ticker(symbol)
    print("{}:{} {}".format(symbol, suffix, ticker))
    data = ticker.info
    # most weird. The original code works fine locally from the laptop, but fails for e.g. ASX as info just has {'logo_url':''}
    # if run as a lambda; but a different call works
    price = 0
    if 'regularMarketPrice' in data:
        raw = data['regularMarketPrice']
        price = round(raw * exchange_rate, 3)
    else:
        data = yf.download(symbol + suffix, period="2d",
            group_by='ticker', actions=False)
        afi=data 
        try:
            key = np.datetime64(date)
            raw = afi.loc[key]['Close']
            price = round(raw * exchange_rate, 3)
        except KeyError:
            key = np.datetime64(previous_date)
            raw = afi.loc[key]['Close']
            price = round(raw * exchange_rate, 3)

    print("{}.{} with suffix {} currency {} for date {} raw {} rate {} exchanged ".format(exchange, symbol, suffix, currency, date, raw, exchange_rate, price))
    
    if save:
        save_price_to_database(exchange, symbol, price)
        save_price_history_to_database(exchange, symbol, date, price)

    return response(
        200,
        {
            "exchange": exchange,
            "symbol": symbol,
            "date": date,
            "raw": raw,
            "exchange_rate": exchange_rate,
            "price": price,
        },
    )


def get_exchange_rate(currency, date):
    if not currency:
        return 1.0
    # I don't know why I always do this, and I'm getting rate warnings on exchange rate
    # url = "{}/exchange-rate/{}/NZD".format(HOST, currency)
    # api_response = requests.post(url)
    url = "{}/exchange-rate/{}/NZD?date={}".format(HOST, currency, date)
    print(url)
    api_response = requests.get(url)
    print(api_response)
    if api_response.status_code != 200:
        print("response code {} so returning None".format(api_response.status_code))
        return None
    print(api_response.json())
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


def get_stock(exchange, symbol, date):
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


def save_price_to_database(exchange, symbol, price):
    payload = {
        'lambda':'stocks',
        'method':'save_price_to_database',
        'data': {
            'exchange':exchange,
            'symbol':symbol,
            'price':price
        }
    }
    print("save_price_to_database")
    print(payload)
    api_response = lambda_client.invoke(
        FunctionName = 'arn:aws:lambda:ap-southeast-2:396194066872:function:database',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(payload)
        )
 
    responseFromChild = json.load(api_response['Payload'])
    print(responseFromChild)


def save_price_history_to_database(exchange, symbol, date, price):
    payload = {
        'lambda':'stocks',
        'method':'save_price_history_to_database',
        'data': {
            'exchange':exchange,
            'symbol':symbol,
            'date':date,
            'price':price
        }
    }
    print("save_price_history_to_database")
    print(payload)
    api_response = lambda_client.invoke(
        FunctionName = 'arn:aws:lambda:ap-southeast-2:396194066872:function:database',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(payload)
        )
 
    responseFromChild = json.load(api_response['Payload'])
    print(responseFromChild)

def update_prices_for_date(event):
    parameters = event["pathParameters"]
    if not "date" in parameters:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        date = parameters["date"]

    holdings_response = requests.get("{}/all_holdings?date={}".format(HOST, date))
    print(holdings_response)
    if holdings_response.status_code != 200:
        return response(holdings_response.status_code, holdings_response.text)
    updates = 0
    for holding in holdings_response.json():
        exchange = holding["exchange"].upper()
        symbol = holding["symbol"].upper()
        update_price(exchange, symbol, date)
        updates = updates + 1
    return response(200,{"updates":updates, "date":date})

def update_price(exchange, symbol, date):
    url = "{}/stocks/{}/{}/{}".format(HOST, exchange, symbol, date)
    price_response = requests.post(url)
    if price_response.status_code != 200:
        print(
            "stocks : could not get price for {}.{} : status {} from url".format(
                exchange, symbol, price_response.status_code, url
            )
        )
        return None
    print(price_response.json())
    return price_response.json()["price"]
