import csv
import json

import dateparser
import psycopg2


def convert_csv_row_to_json(row):
    return {
        'date': dateparser.parse(row[0]),
        'amount': row[1],
        'payee': row[2],
        'particulars': row[3],
        'code': row[4],
        'reference': row[5],
        'transaction_type': row[6],
        'this_account': row[7],
        'other_account': row[8],
        'serial': row[9],
        'transaction_code': row[10],
        'batch_number': row[11],
        'originating_bank': row[12],
        'date_processed': dateparser.parse(row[13])
    }


def convert_database_row_to_json(row):
    return {
        'id': row[0],
        'account_id': row[1],
        'date': row[2],
        'amount': row[3],
        'payee': row[4],
        'particulars': row[5],
        'code': row[6],
        'reference': row[7],
        'transaction_type': row[8],
        'this_account': row[9],
        'other_account': row[10],
        'serial': row[11],
        'transaction_code': row[12],
        'batch_number': row[13],
        'originating_bank': row[14],
        'date_processed': row[15],
        'category': row[16],
        'sub_category': row[16],
    }


def data_exists(data, con, account_id):
    cur = con.cursor()
    cur.execute('SELECT id FROM transaction '
                'WHERE account_id = %s '
                'AND date = %s '
                'AND amount = %s '
                'AND payee = %s',
                [account_id, data['date'], data['amount'], data['payee']])
    rows = cur.fetchall()
    return len(rows) > 0


def maybe_load_row(data, con, account_id):
    if data_exists(data, con, account_id):
        return False
    cur = con.cursor()
    cur.execute('INSERT INTO transaction (account_id, date, amount, payee, particulars, code, reference, '
                'transaction_type, this_account, other_account, serial, transaction_code, batch_number, '
                'originating_bank, date_processed) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
                [account_id,
                 data['date'],
                 data['amount'],
                 data['payee'],
                 data['particulars'],
                 data['code'],
                 data['reference'],
                 data['transaction_type'],
                 data['this_account'],
                 data['other_account'],
                 data['serial'],
                 data['transaction_code'],
                 data['batch_number'],
                 data['originating_bank'],
                 data['date_processed']
                 ])
    con.commit()
    return True


def get_con():
    return psycopg2.connect(database="croesus", user="croesus", password="gold", host="127.0.0.1", port="5432")


def get_categories(con):
    cur = con.cursor()
    cur.execute('SELECT id, category, sub_category, rules FROM category ORDER BY id')
    rows = cur.fetchall()
    categories = []
    for row in rows:
        category = {
            'id': row[0],
            'category': row[1],
            'sub_category': row[2],
            'rules': row[3]
        }
        categories.append(category)
    return categories


def record_matches_category(record, category):
    rules = json.loads(category['rules'])
    column = rules['column']
    operation = rules['operation']
    value = rules['value']
    if operation == 'equals':
        if record[column] == value:
            return True
    return False


def guess_category(record, categories):
    for category in categories:
        if record_matches_category(record, category):
            return category
    return None


def update_row_category(record, category, con):
    cur = con.cursor()
    cur.execute('UPDATE transaction SET category = %s, sub_category = %s WHERE id = %s',
                [category['category'], category['sub_category'], record['id']])
    con.commit()

def setup_categories():
    con = get_con()
    categories = get_categories(con)
    cur = con.cursor()
    sql = 'SELECT id, account_id, date, amount, payee, particulars, code, reference, ' \
          'transaction_type, this_account, other_account, serial, transaction_code, batch_number, ' \
          'originating_bank, date_processed, category, sub_category FROM transaction'
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        record = convert_database_row_to_json(row)
        category = guess_category(record, categories)
        print('{} : {} = {}'.format(record['id'], record['category'], category))
        if category:
            update_row_category(record, category, con)


def import_file(filename, account_id):
    con = get_con()

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 1
        next(csv_reader, None)  # skip headers
        for row in csv_reader:
            data = convert_csv_row_to_json(row)
            if maybe_load_row(data, con, account_id):
                print('loaded row {} : {}'.format(line_count, data))
            else:
                print('skipped row {} '.format(line_count))
            line_count = line_count + 1

    con.commit()

# import_file('../data/Joint-account-22JAN2019-to-22JAN2021.csv', 1)
setup_categories()
