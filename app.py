import pandas as pd
import requests
import subprocess


exit_code = subprocess.call('/home/ali/tmp/analyze-tse/directory.sh')
# print(exit_code)


url = 'http://www.tsetmc.com/tsev2/data/MarketWatchPlus.aspx'
r = requests.get(url)
main_text = r.text


text = main_text.split(';')
rows = [row.split(',') for row in text]
df = pd.DataFrame(rows)



csvs = main_text.split('@')
main_csv = csvs[2]
csv = main_csv.split(';')
rows = [row.split(',') for row in csv]
df = pd.DataFrame(rows)



# df.to_csv('data.csv', index=False)
len(df)



stock_keys = ['300', '303', '305', '309', '380']
main_df = df[df[22].isin(stock_keys)]

main_df.to_csv('/tmp/watchlist/data.csv', index=False)
len(main_df)




import csv
import sqlite3
file = open('/tmp/watchlist/data.csv')
csvreader = csv.reader(file)
header = next(csvreader)
db_rows = []
for row in csvreader:
    db_rows.append(row)
file.close()

conn = sqlite3.connect('/tmp/watchlist/data.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS data')
cur.execute("""CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    one Text ,
    two Text );""")
conn.commit()

def Insert_Data ():

    for i in range(1, len(db_rows)):

        one = str(db_rows[i][2])
        two = str(db_rows[i][22])
        number = i
        query = f'INSERT INTO data VALUES ("{number}", "{one}","{two}")'
        cur.execute(query)
        conn.commit()

    conn.close()

Insert_Data()






import pandas as pd
import csv
import time
import math

stock_keys = [ 'خودرو', 'كگل', 'شستا', 'فولاد', 'شبندر' ]
watch_df = df[df[2].isin(stock_keys)]

watch_df.to_csv('/tmp/watchlist/watch.csv', index=False)

numbers_list = watch_df[2].tolist()

Highـrange = watch_df[19].tolist()
Lowـrange = watch_df[20].tolist()
# numbers_listab = watch_df[12].tolist()
# numbers_listac = watch_df[11].tolist()

# id
# numbers_finalvv = watch_df[0].tolist()

# latest
numbers_latest = watch_df[7].tolist()
# final
numbers_final = watch_df[6].tolist()
# Volume
numbers_final_v = watch_df[9].tolist()

millnames = ['',' Thousand',' Million',' Billion',' Trillion']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

n = 0
Volume_list = []

for i in range(len(numbers_final_v)):
    inf = (int(numbers_final_v[n]))
    Volume_list.append((millify(inf)))
    n+=1

m = 0
for j in range (len(numbers_list)):
    if (numbers_final[m] == numbers_latest[m]):
        #sign = "⚪️"
        state = "="
        sign = "⏸"
    elif (numbers_final[m] > numbers_latest[m]):
        #sign = "🔴"
        state = ">"
        sign = "⏬"
    elif (numbers_final[m] < numbers_latest[m]):
        #sign = "🟢"
        state = "<"
        sign = "⏫"

    final = (numbers_final[m])
    final = f"{int(final):000,}"
    latest = (numbers_latest[m])
    latest = f"{int(latest):000,}"
    high = (Highـrange[m])
    high = round(float(high))
    high = f"{(high):000,}"

    low = (Lowـrange[m])
    low = round(float(low))
    low = f"{(low):000,}"
    print(f"(L={low}  (final={final}{state}latest={latest})  H={high} ,{Volume_list[m]}) = {sign} {numbers_list[m]}")
    m+=1
    time.sleep(0.25)





