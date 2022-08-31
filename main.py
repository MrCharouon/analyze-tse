import argparse
from directory import *
from db_connection import *

directorycheck()
parser = argparse.ArgumentParser(description="""Documentation for the program""", usage="""
      For example:
    \t python main.py --add کگل
    \t python main.py --remove کگل""", epilog="and that's how you'd add and remove stocks on your watchlist")
parser.add_argument('--add', action='store', dest='a_invest', help='add a new invest to datebase')
parser.add_argument('--remove', action='store', dest='r_invest', help='remove a invest from your watchlist')

args = parser.parse_args()
stock_input_add = (args.a_invest)
stock_input_remove = (args.r_invest)
if (stock_input_add != None or stock_input_remove != None):
    if(stock_input_add != None):
        def check(w, list):
            if w in list:
                print("\n"+ "این سهم رو قبلا اضافه کردی")
            else:
                INSERT_DATA(id_keys_list, stock_input_add)
                print("\n"+ 'سهم با موفقیت به پایگاه داده اضافه شد : ' + stock_input_add )

        check(stock_input_add,stock_keys_list)
        result = update_db()
        r = result.update()
        print("\n"+ 'your investments are : ' + str(r)+ "\n")
        exit(0)
    elif(stock_input_remove != None):
        def check(w, list):
            if w in list:
                DELETE_DATA(stock_input_remove)
                print("\n"+ 'سهم با موفقیت از پایگاه داده حذف شد : ' + stock_input_remove)
                
            else:
                print ("\n"+ "چنین سهمی وجود ندارد")

        check(stock_input_remove,stock_keys_list)
        result = update_db()
        r = result.update()
        print("\n"+ 'your investments are : ' + str(r)+ "\n")
        exit(0)
    exit(0)


result = update_db()
result = result.update()
if (len(result) == 0):
    print ("\n"+ "هنوز سهمی اضافه نکرده اید"+ "\n"+ "برای دیدن دستورات بیشتر اجرا کنید"+ "\n"+ "main.py --help"+ "\n")
else:
    # print("\n"+ 'your investments are : ' + str(r)+ "\n")
    import pandas as pd
    import requests
    # import subprocess


    # exit_code = subprocess.call('/home/ali/tmp/analyze-tse/directory.sh')
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

    main_df.to_csv(path_data_csv, index=False)
    len(main_df)




    import csv
    import sqlite3
    file = open(path_data_csv)
    csvreader = csv.reader(file)
    header = next(csvreader)
    db_rows = []
    for row in csvreader:
        db_rows.append(row)
    file.close()

    conn = sqlite3.connect(path_data_db)
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

    # stock_keys = [ 'خودرو', 'شپنا', 'تفارس', 'خساپا', 'شستا','شتران','خمحركه','رافزا','سآبيك','ددانا','كماسه' ]
    watch_df = df[df[2].isin(result)]

    watch_df.to_csv(path_watch_csv, index=False)

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

    millnames = ['',' Th',' M',' B',' T']

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

    list_final = []
    list_latest = []
    list_numbers_list = []
    list_sign = []
    list_Volume_list = []
    # list_low_high= []
    # list_low= []
    # list_high= []
    list_queue = []
    for j in range (len(numbers_list)):
        if (int(numbers_final[m]) == int(numbers_latest[m])):
            #sign = "⚪️"
            state = "="
            sign = " * "
        elif (int(numbers_final[m]) > int(numbers_latest[m])):
            #sign = "🔴"
            state = ">"
            sign = ""
        elif (int(numbers_final[m]) < int(numbers_latest[m])):
            #sign = "🟢"
            state = "<"
            sign = "⏫"

        final = (numbers_final[m])
        final = f"{int(final):000,}"
        list_final.append(final)
        latest = (numbers_latest[m])
        latest = f"{int(latest):000,}"
        list_latest.append(latest)

        list_numbers_list.append(numbers_list[m])
        list_sign.append(sign)

        list_Volume_list.append(Volume_list[m])
        high = (Highـrange[m])
        high = round(float(high))
        high = f"{(high):000,}"
        # list_high.append(high)

        low = (Lowـrange[m])
        low = round(float(low))
        low = f"{(low):000,}"
        # list_low.append(low)

        # list_low_high = list_low + list_high

        if(high == latest):
            list_queue.append("KH")
        elif(low == latest):
            list_queue.append("FR")
        else:
            list_queue.append("")


        # print(f"(L={low}  (final={final}{state}latest={latest})  H={high} ,{Volume_list[m]}) = {sign} {numbers_list[m]}")
        m+=1
        # time.sleep(0.25)

    id_list = []
    m = 1
    for j in range(len(numbers_list)):
        id_list.append(str(m))
        m+=1

    from prettytable import PrettyTable
    columns = ["Id", "Final","Latest", "State", "Volume", "Queue", "Name"]
    newTable = PrettyTable()

    # Add Columns
    newTable.add_column(columns[0], id_list)
    newTable.add_column(columns[1], list_final)
    newTable.add_column(columns[2], list_latest)
    newTable.add_column(columns[3], list_sign)
    newTable.add_column(columns[4], list_Volume_list)
    newTable.add_column(columns[5], list_queue)
    newTable.add_column(columns[6], list_numbers_list)

    print(newTable)
