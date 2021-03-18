import json
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

    value = 0
    holdings = []
    for holding in holdings_response.json():
        exchange = holding["exchange"]
        if filter_exchange and (exchange != filter_exchange):
            continue
        symbol = holding["symbol"]
        if filter_symbol and (symbol != filter_symbol):
            continue
        quantity = holding["quantity"]
        price = get_cached_price(exchange, symbol)
        if not price:
            holding = {
                "exchange": exchange,
                "symbol": symbol,
                "quantity": round(quantity, 2),
                "price": None,
                "value": None,
            }
            holdings.append(holding)
            continue
        value = value + (quantity * price)
        holding = {
            "exchange": exchange,
            "symbol": symbol,
            "quantity": round(quantity, 2),
            "price": price,
            "value": round(quantity * price, 2),
        }
        holdings.append(holding)

    response_data = {"total": round(value, 2), "holdings": holdings}
    return response(200, response_data)


def get_cached_price(exchange, symbol):
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


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
