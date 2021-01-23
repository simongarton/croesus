
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
