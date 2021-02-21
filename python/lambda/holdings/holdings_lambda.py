import boto3
import json
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

    return transactions


def test():
    data = transaction('NZX', 'XXX', '2021-02-21', 10.5, 1.02)
    print(data)
    return response(200, data)


test()
