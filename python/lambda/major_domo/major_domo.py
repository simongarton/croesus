import boto3
import json
from decimal import Decimal
from botocore.exceptions import ClientError


# There is a flaw with this approach, in that the maximum size of an attribute in
# DynamoDB is 400KB.


def response(code, body):
    return {
        'statusCode': code,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(body)
    }


def save_price(exchange, symbol, price):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('stock_price')

    db_response = table.put_item(
        Item={
            'exchange': exchange,
            'symbol': symbol,
            'price': Decimal(str(price)),
        }
    )
    return db_response


def save_price_history(exchange, symbol, date, price):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('stock_price_history')

    try:
        historical_data_response = table.get_item(
            Key={'exchange': exchange, 'symbol': symbol})
    except ClientError as e:
        historical_data_response = {'history': {}}

    try:
        historical_data = historical_data_response['Item']['history']
    except KeyError as e:
        historical_data = {}

    historical_data[date] = Decimal(str(price))
    db_response = table.put_item(
        Item={
            'exchange': exchange,
            'symbol': symbol,
            'history': historical_data,
        }
    )
    return db_response


def test():
    response1 = save_price('NZX', 'XXX', 1.02)
    response2 = save_price_history('NZX', 'XXX', '2021-02-20', 1.03)
    data = {
        'response1': response1,
        'response2': response2
    }
    print(data)
    return response(200, data)


test()
