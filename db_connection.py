import sqlite3
from directory import *

conn = sqlite3.connect(path+ 'data.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS invests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_invests Text );""")
conn.commit()

stock_keys_list = []
id_keys_list = []
sql_select_Query = "select * from invests"
cursor = conn.cursor()
cursor.execute(sql_select_Query)
records = cursor.fetchall()
for row in records:
    id_keys_list.append(row[0])
    stock_keys_list.append(row[1])

def INSERT_DATA(final_number_id, new_invest):
    if len(id_keys_list) == 0:
        final_number_id = 1
    else:
        final_number_id = int(id_keys_list[-1])+1
    query = f'INSERT INTO invests VALUES ("{final_number_id}", "{new_invest}")'
    cur.execute(query)
    conn.commit()

def DELETE_DATA(delete_invest):
    query = f'DELETE FROM invests WHERE user_invests = "{delete_invest}"'
    cur.execute(query)
    conn.commit()

class update_db():
    def update(slef):
        update_invest = []
        sql_select_Query = "select * from invests"
        cursor = conn.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            update_invest.append(row[1])
        conn.close()
        return (update_invest)