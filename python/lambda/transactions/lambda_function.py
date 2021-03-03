import boto3
import json
import os
from botocore.exceptions import ClientError
import dateparser

BUCKET_NAME = 'croesus'

# better error handling
# write to logs


def response(code, body):
    return {
        'statusCode': code,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(body)
    }


def lambda_handler(event, context):

    if not 'pathParameters' in event:
        method = event['requestContext']['http']['method']
        if method == 'GET':
            return get_total_response()
        return response(405, {'error': 'unhandled method'})

    method = event['requestContext']['http']['method']
    parameters = event['pathParameters']

    if method == 'GET':
        return get(parameters)
    if method == 'POST':
        return post(parameters, json.loads(event['body']))
    return response(405, {'error': 'unhandled method'})


def get(parameters):
    if 'symbol' in parameters:
        return get_symbol_response(parameters)
    if 'exchange' in parameters:
        return get_exchange_response(parameters)
    return response(500, {'error': 'get() is lost'})


def post(parameters, body):
    if 'symbol' in parameters:
        return post_symbol(parameters, body)


def get_total_response():
    return response(200, get_total_value())


def get_exchange_response(parameters):
    exchange = parameters['exchange']
    return response(200, get_exchange_value(exchange))


def get_symbol_response(parameters):
    exchange = parameters['exchange']
    symbol = parameters['symbol']
    return response(200, get_symbol_value(exchange, symbol))


def post_symbol(parameters, body):
    exchange = parameters['exchange']
    symbol = parameters['symbol']
    date = body['date']
    quantity = body['quantity']
    price = body['price']
    return response(200, add_transaction(exchange, symbol, date, quantity, price))


def add_transaction(exchange, symbol, date, quantity, price):
    s3_client = boto3.client('s3')
    #KEY_NAME = 'holding-{}-{}.json'.format(exchange, symbol)
    KEY_NAME = 'transactions.json'
    FILE_NAME = '/tmp/' + KEY_NAME

    transactions = []
    try:
        s3_client.download_file(BUCKET_NAME, KEY_NAME, FILE_NAME)
        with open(FILE_NAME, 'r') as input:
            transactions = json.load(input)
    except ClientError as e:
        pass

    # sort out the date format
    date_value = dateparser.parse(date)
    formatted_date = date_value.strftime('%Y-%m-%d')
    transaction = {
        'exchange': exchange,
        'symbol': symbol,
        'date': formatted_date,
        'quantity': quantity,
        'price': price,
    }
    transactions.append(transaction)

    with open(FILE_NAME, 'w') as output:
        json.dump(transactions, output)

    try:
        response = s3_client.upload_file(FILE_NAME, BUCKET_NAME, KEY_NAME)
    except ClientError as e:
        print(e)

    os.remove(FILE_NAME)

    return transactions


def get_holdings():
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(BUCKET_NAME)

    key_names = []
    for object in my_bucket.objects.all():
        if 'holding' in object.key:
            key_names.append(object.key)

    s3_client = boto3.client('s3')

    TEMP_NAME = '/tmp/temp.json'
    transactions = []
    holdings = {}
    for key_name in key_names:
        try:
            s3_client.download_file(BUCKET_NAME, key_name, TEMP_NAME)
            with open(TEMP_NAME, 'r') as input:
                transactions = json.load(input)
            os.remove(TEMP_NAME)
            total = 0
            exchange = '-'
            symbol = '-'
            for transaction in transactions:
                total = total + transaction['amount']
                exchange = transaction['exchange']
                symbol = transaction['symbol']
        except ClientError as e:
            pass
        if not exchange in holdings:
            holdings[exchange] = {}
        holdings[exchange][symbol] = total
    return holdings


def get_exchange_value(exchange):
    values = get_values()
    total = 0
    for value_data in values:
        if value_data['exchange'] == exchange:
            total = total + value_data['value']
    return {'exchange': exchange, 'value': total}


def get_symbol_value(exchange, symbol):
    values = get_values()
    total = 0
    for value_data in values:
        if value_data['exchange'] == exchange:
            if value_data['symbol'] == symbol:
                total = total + value_data['value']
    return {'exchange': exchange, 'symbol': symbol, 'value': total}


def get_exchange_values():
    values = get_values()
    total = 0
    result = {}
    for value_data in values:
        exchange = value_data['exchange']
        if not exchange in result:
            result[exchange] = 0
        result[exchange] = result[exchange] + value_data['value']
    return result


def get_total_value():
    values = get_values()
    total = 0
    for value_data in values:
        total = total + value_data['value']
    return {'value': total}


def get_values():
    s3_client = boto3.client('s3')
    KEY_NAME = 'prices.json'
    FILE_NAME = '/tmp/' + KEY_NAME

    price_data = {}
    try:
        s3_client.download_file(BUCKET_NAME, KEY_NAME, FILE_NAME)
        with open(FILE_NAME, 'r') as input:
            price_data = json.load(input)
        os.remove(FILE_NAME)
    except ClientError as e:
        pass

    holdings = get_holdings()
    values = []
    for exchange, exchange_data in holdings.items():
        for symbol, amount in exchange_data.items():
            price = price_data[exchange][symbol]
            value = price * amount
            data = {
                'exchange': exchange,
                'symbol': symbol,
                'amount': amount,
                'price': price,
                'value': value
            }
            values.append(data)

    return values
