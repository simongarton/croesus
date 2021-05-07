import os
import requests
import json
from datetime import date, datetime, timedelta
import sys
import pytz
import yfinance as yf
import boto3


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
    print("exchange {} symbol {} with suffix {} currency {} for date {} actual_date ".format(exchange, symbol, suffix, currency, date, actual_date))
    ticker = yf.Ticker(symbol + suffix) if suffix else yf.Ticker(symbol)
    data = ticker.info
    exchange_rate = get_exchange_rate(currency, date)
    if exchange_rate == None:
        return response(500, {"message": "no exchange rate for {} on {}".format(currency, date)})
    if not 'regularMarketPrice' in data :
        return response(404, {"exchange": exchange, "symbol": symbol})
    raw = data['regularMarketPrice']
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
    url = "{}/exchange-rate/{}/NZD".format(HOST, currency)
    api_response = requests.post(url)
    url = "{}/exchange-rate/{}/NZD/{}".format(HOST, currency, date)
    api_response = requests.get(url)
    if api_response.status_code != 200:
        return None
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
    api_response = lambda_client.invoke(
        FunctionName = 'arn:aws:lambda:ap-southeast-2:396194066872:function:database',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(payload)
        )
 
    responseFromChild = json.load(api_response['Payload'])
    print(responseFromChild)
