import csv

import dateparser
import psycopg2


def convert_row_to_json(row):
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


def import_file(filename, account_id):
    con = psycopg2.connect(database="croesus", user="croesus", password="gold", host="127.0.0.1", port="5432")

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 1
        next(csv_reader, None)  # skip headers
        for row in csv_reader:
            data = convert_row_to_json(row)
            if maybe_load_row(data, con, account_id):
                print('loaded row {} : {}'.format(line_count,data))
            else:
                print('skipped row {} '.format(line_count))
            line_count = line_count + 1

import_file('../data/Joint-account-1JAN2021-to-22JAN2021.csv', 1)
