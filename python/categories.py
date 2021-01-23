import json

from con import get_con


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
          'originating_bank, date_processed, category, sub_category FROM transaction WHERE category IS NULL'
    cur.execute(sql)
    rows = cur.fetchall()
    updates = 0
    for row in rows:
        record = convert_database_row_to_json(row)
        category = guess_category(record, categories)
        print('{} : {} = {}'.format(record['id'], record['category'], category))
        if category:
            update_row_category(record, category, con)
            updates = updates + 1
    print('checked {} rows and updated {}'.format(len(rows), updates))

setup_categories()
