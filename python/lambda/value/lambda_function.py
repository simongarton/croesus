import json
import psycopg2
import os
import datetime
from datetime import timedelta
import pytz


TIMEZONE = pytz.timezone('Pacific/Auckland')

def lambda_handler(event, context):

    method = event["requestContext"]["http"]["method"]

    parameters = event["pathParameters"] if "pathParameters" in event else {}
    if 'cache'in event['rawPath']:
        return handle_cache(method, parameters)

    path = event['rawPath']
    if path == '/summary':
        return summary()

    if method == 'POST':
        return rebuild_value_table()

    filter_exchange = parameters["exchange"] if "exchange" in parameters else None
    filter_symbol = parameters["symbol"] if "symbol" in parameters else None
    filter_account = parameters["account"] if "account" in parameters else None

    cached = get_cache({"id":path})
    if cached["statusCode"] == 200:
        result = json.loads(cached["body"])
        return result

    response = handle(filter_exchange, filter_symbol, filter_account)
    result = json.loads(response['body'])
    post_cache({"id":path,"value":json.dumps(result)})
    return response


def handle_cache(method, parameters):    
    if method == "GET":
        return get_cache(parameters)
    if method == "POST":
        return post_cache(parameters)    
    if method == "DELETE":
        return empty_cache(parameters)    
    return response(415, {"method":method})


def get_cache(parameters):
    conn = get_database_connection()
    if not conn:
        return response(500,{"message":"no db"})
    
    if not "id" in parameters:
        return response(400,{"message":"no id in parameters"})

    cur = conn.cursor()
    cur.execute(
        "SELECT value FROM cache WHERE id = %s;", 
        [parameters["id"]]
    )

    rows = cur.fetchall()
    if len(rows) == 0:
        return response(404,{})
    return response(200, rows[0][0])


def post_cache(parameters):
    conn = get_database_connection()
    if not conn:
        return response(500,{"message":"no db"})
    
    if not "id" in parameters:
        return response(400,{"message":"no id in parameters"})
    if not "value" in parameters:
        return response(400,{"message":"no value in parameters"})

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cache (id, date, value) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE SET value = %s;", 
        [parameters["id"], datetime.datetime.now(TIMEZONE), parameters["value"], parameters["value"]]
    )

    conn.commit()

    return response(200, parameters["value"])

def empty_cache(parameters):
    conn = get_database_connection()
    if not conn:
        return response(500,{"message":"no db"})
    
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM cache", 
    )

    conn.commit()

    return response(200, {})


def summary():

    cached = get_cache({"id":"summary"})
    if cached["statusCode"] == 200:
        return json.loads(cached["body"])

    share_data = get_share_data()
    other_data = get_other_data()

    other_values = [other_item['value'] for other_item in other_data]
    other_value = round(sum(other_values),2)

    value = {
        "share_value": share_data['all']['total'],
        "share_spend": share_data['all']['spend'],
        "share_gain_loss": share_data['all']['gain_loss'],
        "share_percentage": share_data['all']['percentage'],
        "share_cagr": share_data['all']['cagr'],
        "other_value": other_value,
        "total_value": share_data['all']['total'] + other_value,
        "share_data": share_data,
        "other_data": other_data,
        "updated_at": datetime.datetime.now(TIMEZONE).strftime("%Y-%m-%d")
    }

    post_cache({"id":"summary","value":json.dumps(value)})
    return value

def get_share_data():
    share_data = {}
    for account in ['all', 'helen', 'simon', 'trust']:
        share_data[account] = json.loads(get_share_data_for_account(None if account == 'all' else account))
        share_data[account].pop('holdings')
    return share_data

def get_share_data_for_account(account):
    response = handle(None, None, account)
    return response['body']

def get_other_data():
    other_data = []
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute(
        "SELECT date, account, asset, value::numeric::float8, details FROM other_asset ORDER BY asset, account"
    )
    rows = cur.fetchall()
    for row in rows:
        other_data.append({
            "date":row[0].strftime('%Y-%m-%d'),
            "account":row[1],
            "asset":row[2],
            "value":row[3],
            "details":row[4]
        })
    return other_data

    
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
        print("could not get database connection")
        return None


def handle(filter_exchange, filter_symbol, filter_account):
    todays_date = datetime.datetime.now(TIMEZONE).date()

    database_holdings = get_holdings(
        filter_account, filter_exchange, filter_symbol, todays_date
    )
    if not len(database_holdings):
        return response(200, {})
    total_value = 0
    total_spend = 0
    total_quantity = 0
    total_cagr = 0
    holdings = []
    for holding in database_holdings:
        exchange = holding["exchange"]
        symbol = holding["symbol"]
        quantity = holding["quantity"]
        account = holding["account"]
        spend = holding["value"]
        date = holding["date"]
        total_spend = total_spend + spend
        price = get_price(exchange, symbol)  # from price table, so most recent
        if not price:  # should not happen
            holding = {
                "date": exchange,
                "exchange": date,
                "symbol": symbol,
                "account": account,
                "quantity": round(quantity, 2),
                "price": None,
                "value": None,
                "spend": spend,
            }
            holdings.append(holding)
            continue
        value = quantity * price
        total_value = total_value + value
        gain_loss = value - spend
        if (spend > 0):
            percentage = gain_loss / spend
        else:
            percentage = 0
        days = (datetime.date.today() - holding["date"]).days
        years = days/365
        cagr = round(pow((value/spend),(1/years)) - 1, 4)
        total_cagr = total_cagr + (value * cagr)
        holding = {
            "date": date.strftime('%Y-%m-%d'),
            "exchange": exchange,
            "symbol": symbol,
            "account": account,
            "quantity": round(quantity, 2),
            "price": price,
            "value": round(value, 2),
            "spend": spend,
            "gain_loss": round(gain_loss, 2),
            "percentage": round(percentage, 4),
            "cagr": cagr,
        }
        holdings.append(holding)

    response_data = {
        "total": round(total_value, 2),
        "spend": round(total_spend, 2),
        "gain_loss": round(total_value - total_spend, 2),
        "percentage": round((total_value - total_spend) / total_spend, 4),
        "cagr": round(total_cagr / total_value, 2),
        "holdings": holdings,
    }
    return response(200, response_data)


def get_price(exchange, symbol):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute(
        "SELECT id, exchange, symbol, price::numeric::float8 FROM price WHERE exchange = %s AND symbol = %s",
        [exchange, symbol],
    )
    rows = cur.fetchall()
    if len(rows) == 0:
        return None

    return rows[0][3]


# same code value and spending
def get_spend(filter_exchange, filter_symbol, filter_account):
    conn = get_database_connection()
    if not conn:
        return None

    cur = conn.cursor()
    sql = """
        SELECT date, exchange, symbol, sum(price * quantity)::numeric::float8 AS total
        FROM transaction
        WHERE exchange = %s 
        AND symbol = %s
        AND dividend = FALSE
        GROUP BY date, exchange, symbol
        ORDER BY date, exchange, symbol;
        """
    params = [filter_exchange, filter_symbol]
    if filter_account:
        sql = """
            SELECT date, exchange, symbol, sum(price * quantity)::numeric::float8 AS total
            FROM transaction
            WHERE exchange = %s 
            AND symbol = %s 
            AND account = %s
            AND dividend = FALSE
            GROUP BY date, exchange, symbol
            ORDER BY date, exchange, symbol;
            """
        params = [filter_exchange, filter_symbol, filter_account]
    
    cur.execute(sql, params)
    rows = cur.fetchall()
    total = 0
    data = []
    for row in rows:
        point = {
            "date": row[0],
            "exchange": row[1],
            "symbol": row[2],
            "total": round(row[3], 2),
        }
        data.append(point)
        total = total + row[3]
    return total


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


# same code : value and holdings
def get_holdings(filter_account, filter_exchange, filter_symbol, query_date):
    conn = get_database_connection()
    if not conn:
        return []
    cur = conn.cursor()
    sql = "SELECT id, date, exchange, symbol, account, quantity, price::numeric::float8 FROM transaction ORDER BY date, exchange, symbol"
    params = []
    if filter_account:
        sql = "SELECT id, date, exchange, symbol, account, quantity, price::numeric::float8 FROM transaction WHERE account = %s ORDER BY date, exchange, symbol"
        params = [filter_account]
    cur.execute(sql, params)

    transactions = cur.fetchall()

    holdings = []
    for transaction in transactions:
        transaction_date = transaction[1]
        if transaction_date > query_date:
            continue
        if filter_exchange is not None:
            if transaction[2] != filter_exchange:
                continue
        if filter_symbol is not None:
            if transaction[3] != filter_symbol:
                continue
        date = transaction[1]
        exchange = transaction[2]
        symbol = transaction[3]
        account = transaction[4]
        quantity = transaction[5]
        price = transaction[6]
        holdings.append(
            {
                "date": date,
                "exchange": exchange,
                "symbol": symbol,
                "account": account,
                "quantity": quantity,
                "price": price,
                "value": quantity * price,
            }
        )

    # sort
    holdings.sort(key=lambda x: x["exchange"] + ":" + x["symbol"] + ":" + x["date"].strftime("%Y-%m-%d"))
    return holdings


def empty_value_table():
    conn = get_database_connection()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('delete from value')
    conn.commit()


def find_accounts():
    conn = get_database_connection()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('select distinct account from transaction order by account')
    rows = cur.fetchall()
    return [row[0] for row in rows]

def find_holdings(account):
    conn = get_database_connection()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('select exchange, symbol, min(date) from transaction where account = %s group by exchange, symbol order by exchange, symbol', [account])
    rows = cur.fetchall()
    holdings = []
    for row in rows:
        holding = {
            'exchange':row[0],
            'symbol':row[1],
            'earliest':row[2],
            'account':account
        }
        holdings.append(holding)
    return holdings


def find_transactions(exchange, symbol, account):
    conn = get_database_connection()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('select date, quantity from transaction where exchange = %s and symbol = %s and account = %s',[exchange, symbol, account])
    rows = cur.fetchall()
    transactions = []
    for row in rows:
        transactions.append({
            'date':row[0],
            'quantity':row[1]
        })
    return transactions


def find_prices(exchange, symbol):
    conn = get_database_connection()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('select date, price::numeric::float8 from price_history where exchange = %s and symbol = %s',[exchange, symbol])
    rows = cur.fetchall()
    prices = {}
    for row in rows:
        prices[row[0]] = row[1]
    return prices


def build_value(holding):
    conn = get_database_connection()
    if not conn:
        return []
    cur = conn.cursor()

    exchange = holding['exchange']
    symbol = holding['symbol']
    earliest = holding['earliest']
    account = holding['account']

    transactions = find_transactions(exchange, symbol, account)

    # this is going to get very big
    prices = find_prices(exchange, symbol)
    print("for {}.{} I have {} prices".format(exchange, symbol, len(prices)))

    quantity = 0
    price = 0
    for day in daterange(earliest, datetime.datetime.now(TIMEZONE).date() + datetime.timedelta(days=1)):
        for transaction in transactions:
            if transaction['date'] == day:
                quantity = quantity + transaction['quantity']
        if day in prices:
            price = prices[day]
        value = quantity * price
        #print('on {} for {}:{} ({}) I have q {} p {} v {}'.format(day,exchange, symbol, account, quantity, price, value))
        sql = 'insert into value (date, exchange, symbol, account, price, quantity, value) values (%s,%s,%s,%s,%s,%s,%s)'
        cur.execute(sql, [day, exchange, symbol, account, price, quantity, value])
    conn.commit()


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def rebuild_value_table():
    empty_value_table()
    accounts = find_accounts()
    for account in accounts:
        holdings = find_holdings(account)
        for holding in holdings:
            build_value(holding)
    return response(200, {"message":"value table rebuilt"})