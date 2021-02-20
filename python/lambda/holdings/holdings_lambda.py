import json


def lambda_handler(event, context):

    method = event['requestContext']['http']['method']
    parameters = event['pathParameters']

    if method == 'GET':
        return get(parameters)
    if method == 'POST':
        return post(parameters)
    return {
        'statusCode': 400,
        'body': {'error': 'unhandled method'}
    }


def get(parameters):
    if 'symbol' in parameters:
        return get_symbol(parameters)
    if 'exchange' in parameters:
        return get_exchange(parameters)
    return {
        'statusCode': 200,
        'body': {'message': 'this will get the total holds'}
    }


def post(parameters):
    if 'symbol' in parameters:
        return post_symbol(parameters)
    return {
        'statusCode': 405,
        'body': {'error': 'unhandled method for exchange'}
    }


def get_exchange(parameters):
    exchange = parameters['exchange']
    return {
        'statusCode': 200,
        'body': {'message': 'this will be the total for ' + exchange}
    }


def get_symbol(parameters):
    exchange = parameters['exchange']
    symbol = parameters['symbol']
    return {
        'statusCode': 200,
        'body': {'message': 'this will be the total for ' + exchange + ':' + symbol}
    }


def post_symbol(parameters):
    exchange = parameters['exchange']
    symbol = parameters['symbol']
    return {
        'statusCode': 200,
        'body': {'message': 'this will update ' + exchange + ':' + symbol}
    }
