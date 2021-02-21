import json
import boto3
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


def lambda_handler(event, context):

    method = event['requestContext']['http']['method']
    parameters = event['pathParameters']
    body = event['body']

    if method == 'GET':
        return get(parameters)
    if method == 'POST':
        return post(parameters, body)
    return response(400, {'error': 'unhandled method'})


def get(parameters):
    if 'symbol' in parameters:
        return get_symbol(parameters)
    if 'exchange' in parameters:
        return get_exchange(parameters)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('holdings')
    table_response = table.scan()
    items = table_response['Items']
    while 'LastEvaluatedKey' in table_response:
        table_response = table.scan(
            ExclusiveStartKey=table_response['LastEvaluatedKey'])
        items.extend(response['Items'])

    return response(200, items)


def get_exchange(parameters):
    exchange = parameters['exchange']
    return response(200, {'message': 'this will get the total holds for the exchange {}'.format(exchange)})


def get_symbol(parameters):
    exchange = parameters['exchange']
    symbol = parameters['symbol']
    return response(200, {'message': 'this will get the total holds for the exchange {} and symbol {}'.format(exchange, symbol)})


def post(parameters, body):
    for key in ['exchange', 'symbol']:
        if not key in parameters:
            return response(400, {'error': 'no {} in parameters'.format(key)})

    for key in ['date', 'amount', 'price']:
        if not key in body:
            return response(400, {'error': 'no {} in body'.format(key)})

    exchange = parameters['exchange']
    symbol = parameters['symbol']
    date = body['date']
    amount = body['amount']
    price = body['price']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('holdings')

    try:
        holdings_response = table.get_item(
            Key={'exchange': exchange, 'symbol': symbol})
    except ClientError as e:
        holdings_response = {'holdings': {}}

    try:
        holdings = holdings_response['Item']['history']
    except KeyError as e:
        holdings = []

    holding = {
        'date': date,
        'amount': str(amount),
        'price': str(price)

    }
    holdings.append(holding)
    print(holdings)
    db_response = table.put_item(
        Item={
            'exchange': exchange,
            'symbol': symbol,
            'history': holdings,
        }
    )
    return response(200, holdings)


def test_post():
    path_parameters = {
        'exchange': 'NZX',
        'symbol': 'YYY',
    }

    body = {
        'date': '2021-02-21',
        'amount': 10.5,
        'price': 1.37,

    }

    print(post(path_parameters, body))


def test_get():
    path_parameters = {
    }
    print(get(path_parameters))


test_get()
