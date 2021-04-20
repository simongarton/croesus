import json
import psycopg2
import os
import datetime
from datetime import timedelta
import pytz


TIMEZONE = pytz.timezone('Pacific/Auckland')

def lambda_handler(event, context):

    method = event["requestContext"]["http"]["method"]
    if method == 'POST':
        return rebuild_value_table()

    if not "pathParameters" in event:
        return response(400, {"error": "no path parameters : need account"})
    parameters = event["pathParameters"]
    if not "account" in parameters:
        return response(400, {"error": "no path parameters : need account"})
    filter_exchange = parameters["exchange"] if "exchange" in parameters else None
    filter_symbol = parameters["symbol"] if "symbol" in parameters else None
    filter_account = parameters["account"]

    return handle(filter_exchange, filter_symbol, filter_account)


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
    # need to include filter account - and now I need to go straight to the database, not use the API.
    todays_date = datetime.datetime.now(TIMEZONE).date()

    database_holdings = get_holdings(
        filter_account, filter_exchange, filter_symbol, todays_date
    )
    if not len(database_holdings):
        return response(200, [])
    total_value = 0
    total_spend = 0
    holdings = []
    for holding in database_holdings:
        exchange = holding["exchange"]
        symbol = holding["symbol"]
        quantity = holding["quantity"]
        account = holding["account"]
        spend = get_spend(exchange, symbol, account)
        total_spend = total_spend + spend
        price = get_price(exchange, symbol)  # from price table, so most recent
        if not price:  # should not happen
            holding = {
                "exchange": exchange,
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
        percentage = gain_loss / spend
        holding = {
            "exchange": exchange,
            "symbol": symbol,
            "account": account,
            "quantity": round(quantity, 2),
            "price": price,
            "value": round(value, 2),
            "spend": spend,
            "gain_loss": round(gain_loss, 2),
            "percentage": round(percentage, 4),
        }
        holdings.append(holding)

    response_data = {
        "total": round(total_value, 2),
        "spend": round(total_spend, 2),
        "gain_loss": round(total_value - total_spend, 2),
        "percentage": round((total_value - total_spend) / total_spend, 4),
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
        WHERE exchange = %s AND symbol = %s
        GROUP BY date, exchange, symbol
        ORDER BY date, exchange, symbol;
        """
    params = [filter_exchange, filter_symbol]
    if filter_account != 'all':
        sql = """
            SELECT date, exchange, symbol, sum(price * quantity)::numeric::float8 AS total
            FROM transaction
            WHERE exchange = %s AND symbol = %s AND account = %s
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
def get_holdings(account, exchange, symbol, query_date):
    conn = get_database_connection()
    if not conn:
        return []
    cur = conn.cursor()
    sql = "SELECT id, date, exchange, symbol, account, quantity, price FROM transaction ORDER BY date, exchange, symbol"
    params = []
    if account != "all":
        sql = "SELECT id, date, exchange, symbol, account, quantity, price FROM transaction WHERE account = %s ORDER BY date, exchange, symbol"
        params = [account]
    cur.execute(sql, params)

    transactions = cur.fetchall()

    holdings_map = {}

    for transaction in transactions:
        transaction_date = transaction[1]
        if transaction_date > query_date:
            continue
        if exchange is not None:
            if transaction[2] != exchange:
                continue
        if symbol is not None:
            if transaction[3] != symbol:
                continue
        key = transaction[2] + ":" + transaction[3] + ":" + transaction[4]
        if not key in holdings_map:
            holdings_map[key] = 0
        holdings_map[key] = holdings_map[key] + transaction[5]

    holdings = []
    for key, value in holdings_map.items():
        parts = key.split(":")
        exchange = parts[0]
        symbol = parts[1]
        account = parts[2]
        holdings.append(
            {
                "exchange": exchange,
                "symbol": symbol,
                "account": account,
                "quantity": value,
            }
        )

    # sort
    holdings.sort(key=lambda x: x["exchange"] + ":" + x["symbol"])
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