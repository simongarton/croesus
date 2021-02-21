import boto3
import json
import os
from botocore.exceptions import ClientError

BUCKET_NAME = 'croesus'

# better error handling
# logs


def response(code, body):
    return {
        'statusCode': code,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(body)
    }


def transaction(exchange, symbol, date, amount, price):

    s3_client = boto3.client('s3')
    FILE_NAME = 'holding-{}-{}.json'.format(exchange, symbol)

    transactions = []
    try:
        s3_client.download_file(BUCKET_NAME, FILE_NAME, FILE_NAME)
        with open(FILE_NAME, 'r') as input:
            transactions = json.load(input)
    except ClientError as e:
        pass

    transaction = {
        'exchange': exchange,
        'symbol': symbol,
        'date': date,
        'amount': amount,
        'price': price,
    }
    transactions.append(transaction)

    with open(FILE_NAME, 'w') as output:
        json.dump(transactions, output)

    try:
        response = s3_client.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
    except ClientError as e:
        print(e)

    os.delete(FILE_NAME)

    return transactions


def get_holdings():
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(BUCKET_NAME)

    files = []
    for file in my_bucket.objects.all():
        if 'holding' in file.key:
            files.append(file.key)

    s3_client = boto3.client('s3')

    TEMP_NAME = 'temp.json'
    transactions = []
    holdings = {}
    for file_name in files:
        try:
            s3_client.download_file(BUCKET_NAME, file_name, TEMP_NAME)
            with open(TEMP_NAME, 'r') as input:
                transactions = json.load(input)
            os.delete(TEMP_NAME)
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
    FILE_NAME = 'prices.json'

    price_data = {}
    try:
        s3_client.download_file(BUCKET_NAME, FILE_NAME, FILE_NAME)
        with open(FILE_NAME, 'r') as input:
            price_data = json.load(input)
        os.delete(FILE_NAME)
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


def test():
    #data = transaction('NZX', 'XXX', '2021-02-21', 10.5, 1.02)
    data = get_holdings()
    print(get_values())
    print(get_total_value())
    print(get_exchange_values())
    print(get_exchange_value('NZX'))
    print(get_exchange_value('NYSE'))
    return response(200, data)


test()
