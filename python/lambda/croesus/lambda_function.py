import json
import datetime
import boto3

lambda_client = boto3.client('lambda')

def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=date_converter),
    }


def date_converter(o):
    if isinstance(o, datetime.datetime):
        return o.strftime("%Y-%m-%d")
    if isinstance(o, datetime.date):
        return o.strftime("%Y-%m-%d")
    return "{}".format(o)


def lambda_handler(event, context):
    
    method = event["requestContext"]["http"]["method"]
    parameters = event["pathParameters"] if "pathParameters" in event else {}

    if method == "GET":
        return get(parameters)
    if method == "POST":
        return password(parameters, json.loads(event["body"]))
    return response(405, {"error": "unhandled method"})


def get(parameters):
    return {
        'statusCode': 200,
        'body': json.dumps('rich as, bro')
    }


def password(parameters, body):
    if not 'password' in body:
        log('croesus', 'password', 400)
        return response(400,{"message":"no password"})
    payload = {
        'lambda':'croesus',
        'method':'password',
        'data': {
            'password':body['password']
        }
    }
    # this should become a common methof
    api_response = lambda_client.invoke(
        FunctionName = 'arn:aws:lambda:ap-southeast-2:396194066872:function:database',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(payload)
        )
 
    responseFromChild = json.load(api_response['Payload'])
    log('croesus', 'password', responseFromChild['statusCode'])
    return response(responseFromChild['statusCode'], json.loads(responseFromChild['body']))


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
