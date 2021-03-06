import json
import psycopg2
import os

# must have VPC and RDS security groups


def lambda_handler(event, context):
    try:
        dbname = os.environ.get('PGDATABASE')
        user = os.environ.get('PGUSER')
        host = os.environ.get('PGHOST')
        password = os.environ.get('PGPASSWORD')
        connection = "dbname='{}' user='{}' host='{}' password='{}'".format(
            dbname, user, host, password)
        conn = psycopg2.connect(connection)
        cur = conn.cursor()
        sql = 'select * from price'
        cur.execute(sql)
        rows = cur.fetchall()
        return {
            'statusCode': 200,
            'body': json.dumps(rows)
        }

    except:
        return {
            'statusCode': 500,
            'body': json.dumps('no connection')
        }
