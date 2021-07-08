import os
import requests
import json
from datetime import date, datetime, timedelta
import psycopg2
import sys
import pytz
import boto3

API_KEY = "d3dce964c1b31b848333b69d"
TIMEZONE = pytz.timezone('Pacific/Auckland')
lambda_client = boto3.client('lambda')


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }

def lambda_handler(event, context):
    if not "pathParameters" in event:
        return {"statusCode": 400, "body": {"message": "no pathParameters"}}
    parameters = event["pathParameters"]
    for param in ["source", "target"]:
        if not param in parameters:
            return {
                "statusCode": 400,
                "body": {"message": "no {} in parameters".format(param)},
            }
    source = parameters["source"].upper()
    target = parameters["target"].upper()
    method = event["requestContext"]["http"]["method"]

    if method == "POST":
        return post_rate(source, target)
    # only applies to GET
    query_parameters = event["queryStringParameters"]
    if "date" in query_parameters:
        return get_rate(source, target, query_parameters["date"])
    rate = get_current_rate(source, target)
    return response(
        200,
        {"source": source, "target": target, "date": datetime.now().strftime("%Y-%m-%d"), "rate": rate},
    )


def get_rate(source, target, date):
    payload = {
        'lambda':'exchange_rate',
        'method':'get_rate',
        'data': {
            'source':source,
            'target':target,
            'date':date
        }
    }
    api_response = lambda_client.invoke(
        FunctionName = 'arn:aws:lambda:ap-southeast-2:396194066872:function:database',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(payload)
        )
 
    responseFromChild = json.load(api_response['Payload'])
    print("get_rate()")
    print(responseFromChild)
    return response(responseFromChild['statusCode'], json.loads(responseFromChild['body']))


def post_rate(source, target):
    rate = get_current_rate(source, target)
    # picking up UTC time ...
    date = datetime.now(TIMEZONE).strftime("%Y-%m-%d")
    save_rate_to_database(source, target, date, rate)
    return response(
        200,
        {"source": source, "target": target, "date": date, "rate": rate},
    )

def get_current_rate(source, target):
    url = "https://v6.exchangerate-api.com/v6/{}/pair/{}/{}".format(API_KEY, source, target)
    print("getting current rate from {}".format(url))
    api_response = requests.get(url)
    api_response.raise_for_status()
    rate = api_response.json()["conversion_rate"]
    return rate


def save_rate_to_database(source, target, date, rate):
    payload = {
        'lambda':'exchange_rate',
        'method':'save_rate_to_database',
        'data': {
            'source':source,
            'target':target,
            'date':date,
            'rate':rate,
        }
    }
    api_response = lambda_client.invoke(
        FunctionName = 'arn:aws:lambda:ap-southeast-2:396194066872:function:database',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(payload)
        )
 
    responseFromChild = json.load(api_response['Payload'])
    print(responseFromChild)
    return response(200, json.loads(responseFromChild['body']))