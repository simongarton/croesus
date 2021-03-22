import os
import requests
import json
from datetime import date, datetime, timedelta
import psycopg2
import sys

HOST = "https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com"
API_KEY = "d3dce964c1b31b848333b69d"


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def get_database_connection():
    try:
        dbname = os.environ.get("PGDATABASE")
        user = os.environ.get("PGUSER")
        host = os.environ.get("PGHOST")
        password = os.environ.get("PGPASSWORD")
        connection = "dbname='{}' user='{}' host='{}' password='{}'".format(
            dbname, user, host, password
        )
        conn = psycopg2.connect(connection)
        return conn
    except:
        return response(500, "connection error : {}".format(sys.exc_info()[0]))


def lambda_handler(event, context):
    print("starting exchange-rate")
    if not "pathParameters" in event:
        print("no path params")
        return {"statusCode": 400, "body": {"message": "no pathParameters"}}
    parameters = event["pathParameters"]
    for param in ["source", "target"]:
        if not param in parameters:
            print("no param {}".format(param))
            return {
                "statusCode": 400,
                "body": {"message": "no {} in parameters".format(param)},
            }
    source = parameters["source"].upper()
    target = parameters["target"].upper()
    method = event["requestContext"]["http"]["method"]

    if method == "POST":
        print("POST exchange-rate : {} {} {}".format(source, target, method))
        return post_rate(source, target)
    # only applies to GET
    date = parameters["date"]
    print("GET exchange-rate : {} {} {} {}".format(source, target, date, method))
    return get_rate(source, target, date)


def post_rate(source, target):
    url = "https://v6.exchangerate-api.com/v6/{}/latest/{}".format(API_KEY, source)
    api_response = requests.get(url)
    api_response.raise_for_status()
    conversion_rates = api_response.json()["conversion_rates"]
    if not target in conversion_rates:
        return response(404, "{} not found with source {}".format(target, source))
    rate = conversion_rates[target]
    # picking up UTC time ...
    date = datetime.now().strftime("%Y-%m-%d")
    save_rate_to_database(source, target, date, rate)
    return response(
        200,
        {"source": source, "target": target, "date": date, "rate": rate},
    )


def get_rate(source, target, date):
    conn = get_database_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute(
        'SELECT rate FROM "exchange-rate" WHERE source = %s AND target = %s AND date = %s;',
        [source, target, date],
    )
    rows = cur.fetchall()
    print("1 {}".format(len(rows)))
    if len(rows) > 0:
        return response(
            200,
            {"source": source, "target": target, "date": date, "rate": rows[0][0]},
        )
    cur.execute(
        'SELECT rate FROM "exchange-rate" WHERE target = %s AND source = %s AND date = %s;',
        [source, target, date],
    )
    rows = cur.fetchall()
    print("2 {}".format(len(rows)))
    if len(rows) > 0:
        return response(
            200,
            {
                "source": source,
                "target": target,
                "date": date,
                "rate": round(1 / rows[0][0], 3),
            },
        )
    return response(
        404, "{} not found with source {} on {}".format(target, source, date)
    )


def save_rate_to_database(source, target, date, rate):
    conn = get_database_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute(
        'SELECT id FROM "exchange-rate" WHERE source = %s AND target = %s AND date = %s;',
        [source, target, date],
    )
    rows = cur.fetchall()
    if len(rows) > 0:
        print("updating {}->{} on {} to {}".format(source, target, date, rate))
        cur.execute(
            'UPDATE "exchange-rate" SET rate = %s WHERE source = %s AND target = %s AND date = %s;',
            [rate, source, target, date],
        )
    else:
        print("inserting {}->{} on {} to {}".format(source, target, date, rate))
        cur.execute(
            'INSERT INTO "exchange-rate" (source, target, date, rate) VALUES (%s, %s, %s, %s);',
            [source, target, date, rate],
        )
    conn.commit()