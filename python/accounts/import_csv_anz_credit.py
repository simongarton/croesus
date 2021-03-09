import csv
import sys
import dateparser

from common import maybe_load_row
from con import get_con


# Card,Type,Amount,Details,TransactionDate,ProcessedDate,ForeignCurrencyAmount,ConversionCharge

def convert_csv_row_to_json(row):
    return {
        'date': dateparser.parse(row[4], settings={'DATE_ORDER': 'DMY'}),
        'amount': get_value(row[2]),
        'payee': row[3].strip(),
        'particulars': None,
        'code': None,
        'reference': None,
        'transaction_type': row[1],
        'this_account': None,
        'other_account': None,
        'serial': None,
        'transaction_code': None,
        'batch_number': None,
        'originating_bank': None,
        'date_processed': None,
        'foreign_currency_amount': row[6],
        'conversion_charge': row[7]
    }


def get_value(value):
    if value == '':
        return 0
    return -(float(value.strip()))


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


import_file(sys.argv[1], 3)
