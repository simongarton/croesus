import json
import requests
import datetime
import random
import time
import os
import sys
import pytz
import boto3


lambda_client = boto3.client('lambda')

TIMEZONE = pytz.timezone('Pacific/Auckland')
HOST = "https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com"


# better error handling
# logs

def lambda_handler(event, context):

    # do exchange rate once a day
    right_now = datetime.datetime.now(TIMEZONE).strftime("%H")
    if right_now == "01" or right_now == "12":
        print("updating exchange rates {}".format(right_now))
        post_todays_exchange_rate("USD", "NZD")
        post_todays_exchange_rate("AUD", "NZD")
    else:
        print("not updating exchange rates {}".format(right_now))

    # get holdings
    todays_date = datetime.datetime.now(TIMEZONE).strftime("%Y-%m-%d")
    holdings_response = requests.get("{}/all_holdings?date={}".format(HOST, todays_date))
    print("holdings")
    print(holdings_response)
    if holdings_response.status_code != 200:
        return response(holdings_response.status_code, holdings_response.text)

    updates = 0
    for holding in holdings_response.json():
        exchange = holding["exchange"].upper()
        symbol = holding["symbol"].upper()
        update_price(exchange, symbol, todays_date)
        updates = updates + 1

    # and rebuild value table
    print("updating value table")
    rebuild_value_table()

    # and empty the caches
    print("emptying caches")
    empty_caches()

    # and repopulate the caches
    print("repopulating caches")
    repopulate_caches()

    # and repopulate the caches
    print("calculating net worth")
    calculate_net_worth()

    print("major_domo done")
    return response(200, {"message": "{} prices updated".format(updates)})


def empty_caches():
    url = "{}/cache".format(HOST)
    print("emptying caches : {}".format(url))
    requests.delete(url)
    print("emptied caches.")
    log('major_domo','empty_caches()', 200)


def calculate_net_worth():
    print("calculating net worth ...")
    data = requests.get("{}/summary".format(HOST))
    payload = {
        'lambda':'major_domo',
        'method':'net_worth',
        'data': data.json()
    }
    print(payload)
    api_response = lambda_client.invoke(
        FunctionName = 'arn:aws:lambda:ap-southeast-2:396194066872:function:database',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(payload)
        )
 
    responseFromChild = json.load(api_response['Payload'])


def repopulate_caches():
    print("repopulating caches ...")
    requests.get("{}/summary".format(HOST))
    requests.get("{}/all_value".format(HOST))
    requests.get("{}/value/helen".format(HOST))
    requests.get("{}/value/simon".format(HOST))
    requests.get("{}/value/trust".format(HOST))
    print("repopulated caches.")
    log('major_domo','repopulate_caches()', 200)
    

def post_todays_exchange_rate(source, target):
    url = "{}/exchange-rate/{}/{}".format(HOST, source, target)
    print("updating exchange rate : {}".format(url))
    requests.post(url)
    print("updated exchange rate.")
    log('major_domo','post_todays_exchange_rate()', 200)


def rebuild_value_table():
    url = "{}/value".format(HOST)
    print("rebuilding value table : {}".format(url))
    requests.post(url)
    print("rebuilt value table.")
    log('major_domo','rebuild_value_table()', 200)


def update_price(exchange, symbol, date):
    url = "{}/stocks/{}/{}/{}".format(HOST, exchange, symbol, date)
    price_response = requests.post(url)
    if price_response.status_code != 200:
        print(
            "major-domo : could not get price for {}.{} : status {} from {}".format(
                exchange, symbol, price_response.status_code, url
            )
        )
        return None
    price = price_response.json()["price"] 
    print(
        "major-domo : got price for {}.{} : status {} from {}".format(
            exchange, symbol, price_response.status_code, url
        )
    )
    return price


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }

# this is a common method
def log(source, details, status_code):
    payload = {
        'lambda':'log',
        'data': {
            'source':source,
            'details':details,
            'status_code':status_code
        }
    }
    api_response = lambda_client.invoke(
        FunctionName = 'arn:aws:lambda:ap-southeast-2:396194066872:function:database',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(payload)
        )
 
    responseFromChild = json.load(api_response['Payload'])
    return response(responseFromChild['statusCode'], json.loads(responseFromChild['body']))
