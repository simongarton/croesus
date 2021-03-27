import csv
import sys
import dateparser

from con import get_con
from common import maybe_load_row


# Date,Amount,Payee,Particulars,Code,Reference,Tran Type,This Party Account,Other Party Account,Serial,Transaction Code,Batch Number,Originating Bank/Branch,Processed Date


def convert_csv_row_to_json(row):
    return {
        "date": dateparser.parse(row[0], settings={"DATE_ORDER": "DMY"}),
        "amount": row[1],
        "payee": row[2],
        "particulars": row[3],
        "code": row[4],
        "reference": row[5],
        "transaction_type": row[6],
        "this_account": row[7],
        "other_account": row[8],
        "serial": row[9],
        "transaction_code": row[10],
        "batch_number": row[11],
        "originating_bank": row[12],
        "date_processed": dateparser.parse(row[13], settings={"DATE_ORDER": "DMY"}),
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
            print(data)
            if maybe_load_row(data, con, account_id):
                print("loaded row {} : {}".format(line_count, data))
            else:
                print("skipped row {} as already got".format(line_count))
            line_count = line_count + 1

    con.commit()


import_file(sys.argv[1], 1)
