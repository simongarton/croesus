import csv
import sys

import dateparser

from common import maybe_load_row
from con import get_con


# Type,Details,Particulars,Code,Reference,Amount,Date,ForeignCurrencyAmount,ConversionCharge


def convert_csv_row_to_json(row):
    return {
        "date": dateparser.parse(row[6], settings={"DATE_ORDER": "DMY"}),
        "amount": row[5],
        "payee": row[1],
        "particulars": row[2],
        "code": row[3],
        "reference": row[4],
        "transaction_type": row[0],
        "this_account": None,
        "other_account": None,
        "serial": None,
        "transaction_code": None,
        "batch_number": None,
        "originating_bank": None,
        "date_processed": None,
        "foreign_currency_amount": None,
        "conversion_charge": None,
    }


def import_file(filename, account_id):
    con = get_con()

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 1
        next(csv_reader, None)  # skip headers
        for row in csv_reader:
            data = convert_csv_row_to_json(row)
            if maybe_load_row(data, con, account_id):
                print("loaded row {} : {}".format(line_count, data))
            else:
                print("skipped row {} as already got".format(line_count))
            line_count = line_count + 1

    con.commit()


import_file(sys.argv[1], 2)
