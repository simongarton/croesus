import dateparser
import datetime

from con import get_con


# using the price history table, fix up any missing entries in value

def has_value(exchange, symbol, date):
    sql = 'SELECT id FROM value WHERE exchange = %s AND symbol = %s AND date = %s;'
    conn = get_con()
    cursor = conn.cursor()
    cursor.execute(sql, [
        exchange, symbol, date
    ])
    rows = cursor.fetchall()
    return len(rows) > 0


def get_price(exchange, symbol, date):
    sql = 'SELECT price::numeric::float8 FROM price_history WHERE exchange = %s AND symbol = %s AND date = %s;'
    conn = get_con()
    cursor = conn.cursor()
    cursor.execute(sql, [
        exchange, symbol, date
    ])
    rows = cursor.fetchall()
    if len(rows) == 0:
        return None
    return rows[0][0]


def get_quantity(exchange, symbol, date):
    sql = 'SELECT sum(quantity) FROM transaction WHERE exchange = %s AND symbol = %s AND date <= %s;'
    conn = get_con()
    cursor = conn.cursor()
    cursor.execute(sql, [
        exchange, symbol, date
    ])
    rows = cursor.fetchall()
    if len(rows) == 0:
        return None
    return rows[0][0]


def add_record(exchange, symbol, date, price, quantity):
    sql = 'INSERT INTO value (date, exchange, symbol, price, quantity, value) VALUES (%s, %s, %s, %s, %s, %s);'
    conn = get_con()
    cursor = conn.cursor()
    cursor.execute(sql, [
        date, exchange, symbol, price, quantity, round(price * quantity, 2)
    ])
    conn.commit()


def catch_up(exchange, symbol):
    start_date = dateparser.parse('01/Jan/2021').date()
    current_price = None
    while start_date < datetime.date.today():

        start_date = start_date + datetime.timedelta(days=1)
        quantity = get_quantity(exchange, symbol, start_date)
        if not quantity or quantity == 0:
            print('{}.{} has no quantity on {} so skipping'.format(
                exchange, symbol, start_date))
            continue
        price = get_price(exchange, symbol, start_date)
        if price:
            current_price = price
        if has_value(exchange, symbol, start_date):
            print('{}.{} has value on {} already so skipping'.format(
                exchange, symbol, start_date))
            continue
        print('{} {} {}'.format(quantity, price, current_price))
        if not price:
            if not current_price:
                print('{}.{} has no price or current price available on {} so skipping'.format(
                    exchange, symbol, start_date))
                continue
            price = current_price
        print("    I could add {} * {} = {} for {}.{} on {}".format(price,
                                                                    quantity, price * quantity, exchange, symbol, start_date))
        add_record(exchange, symbol, start_date, price, quantity)


def has_total(date):
    sql = 'SELECT id FROM total_value WHERE date = %s;'
    conn = get_con()
    cursor = conn.cursor()
    cursor.execute(sql, [
        date
    ])
    rows = cursor.fetchall()
    return len(rows) > 0


def update_total(date, value):
    print('updating total of {} on {}'.format(value, date))
    sql = 'UPDATE total_value SET value = %s WHERE date = %s;'
    conn = get_con()
    cursor = conn.cursor()
    cursor.execute(sql, [
        value,
        date
    ])
    conn.commit()


def add_total(date, value):
    print('adding total of {} on {}'.format(value, date))
    sql = 'INSERT INTO total_value (date, value) VALUES (%s, %s);'
    conn = get_con()
    cursor = conn.cursor()
    cursor.execute(sql, [
        date,
        value
    ])
    conn.commit()


def fix_up_totals():
    sql = 'SELECT date, sum(value) FROM value v GROUP BY date ORDER BY date;'
    conn = get_con()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    for row in rows:
        date = row[0]
        total = row[1]
        if has_total(date):
            update_total(date, total)
        else:
            add_total(date, total)


def run():
    sql = 'SELECT DISTINCT exchange, symbol FROM transaction ORDER BY exchange, symbol;'
    conn = get_con()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    for row in rows:
        exchange = row[0]
        symbol = row[1]
        catch_up(exchange, symbol)

    fix_up_totals()


def test():
    catch_up('NZX', 'NZG')


run()
