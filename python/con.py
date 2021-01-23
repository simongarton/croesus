import psycopg2

def get_con():
    return psycopg2.connect(database="croesus", user="croesus", password="gold", host="127.0.0.1", port="5432")
