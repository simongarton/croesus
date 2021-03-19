import json
from re import S
import requests
import datetime

HOST = "https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com"


# better error handling
# logs


def lambda_handler(event, context):

    if "pathParameters" in event:
        parameters = event["pathParameters"]
        filter_exchange = parameters["exchange"] if "exchange" in parameters else None
        filter_symbol = parameters["symbol"] if "symbol" in parameters else None
        print("got {} and {}".format(filter_exchange, filter_symbol))
    else:
        filter_exchange = None
        filter_symbol = None

    return handle(filter_exchange, filter_symbol)


def handle(filter_exchange, filter_symbol):
    # for now, limit to today otherwise no way of getting value
    todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
    holdings_response = requests.get("{}/holdings?date={}".format(HOST, todays_date))
    if holdings_response.status_code != 200:
        print(holdings_response)
        return response(holdings_response.status_code, holdings_response.text)

    total_value = 0
    total_spend = 0
    holdings = []
    for holding in holdings_response.json():
        exchange = holding["exchange"]
        if filter_exchange and (exchange != filter_exchange):
            continue
        symbol = holding["symbol"]
        if filter_symbol and (symbol != filter_symbol):
            continue
        quantity = holding["quantity"]
        spend = get_spend(exchange, symbol)
        total_spend = total_spend + spend
        price = get_price(exchange, symbol)
        if not price:
            holding = {
                "exchange": exchange,
                "symbol": symbol,
                "quantity": round(quantity, 2),
                "price": None,
                "value": None,
                "spend": spend,
            }
            holdings.append(holding)
            continue
        value = quantity * price
        total_value = total_value + value
        gain_loss = value - spend
        percentage = gain_loss / spend
        holding = {
            "exchange": exchange,
            "symbol": symbol,
            "quantity": round(quantity, 2),
            "price": price,
            "value": round(value, 2),
            "spend": spend,
            "gain_loss": round(gain_loss, 2),
            "percentage": round(percentage, 4),
        }
        holdings.append(holding)

    response_data = {
        "total": round(total_value, 2),
        "spend": round(total_spend, 2),
        "gain_loss": round(total_value - total_spend, 2),
        "percentage": round((total_value - total_spend) / total_spend, 4),
        "holdings": holdings,
    }
    return response(200, response_data)


def get_price(exchange, symbol):
    price_response = requests.get("{}/stocks/{}/{}".format(HOST, exchange, symbol))
    if price_response.status_code != 200:
        print(
            "could not get price for {}.{} : status {}".format(
                exchange, symbol, price_response.status_code
            )
        )
        return None
    print(price_response.json())
    return price_response.json()["price"]


def get_spend(exchange, symbol):
    spend_response = requests.get("{}/spending/{}/{}".format(HOST, exchange, symbol))
    if spend_response.status_code != 200:
        print(
            "could not get price for {}.{} : status {}".format(
                exchange, symbol, spend_response.status_code
            )
        )
        return None
    print(spend_response.json())
    total = 0
    for spend in spend_response.json():
        total = total + spend["total"]
    return total


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
