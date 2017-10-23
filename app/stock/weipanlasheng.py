#encoding=utf-8
# 判断尾盘30min 拉升3%

import tushare as ts
import datetime
import MySQLdb as mdb
import pandas as pd

from app.stock.utils import getYesterday


def _ifLasheng(stockid='000001', date='2017-10-15'):
    '''get one days weipan change'''
    
    now = datetime.datetime.strptime(date, '%Y-%m-%d')
    nowPlusOne = now + datetime.timedelta(days = 1)

    nowStr = now.strftime('%Y-%m-%d')
    nowPlusOneStr = nowPlusOne.strftime('%Y-%m-%d')

    closeData = ts.get_hist_data(stockid, start=nowStr, end=nowPlusOneStr, ktype='30').iloc[0,:]

    change = closeData['price_change']/closeData['open']

    if change >= 0.03:
        return 1
    elif change <= -0.03:
        return -1
    else:
        return 0


def stockLasheng(date = '2017-10-15'):
    '''
    计算多日拉升
    '''    
    stockBasic = ts.get_stock_basics()
    stockAllId = stockBasic.index
    stockName =  stockBasic['name'].values.tolist()
    
    
    symbols = []
    for sid,sname in zip(stockAllId, stockName):
        try:
            print("[info] begin to get {}".format(sid))
            lasheng = _ifLasheng(sid,date)
        except Exception as e:
            lasheng = False
            print("[error] {}".format(e))
        if lasheng != 0:
            symbols.append(
                    (sid,sname,date,lasheng)
                    )

    return symbols



def intoDB(symbols):
    '''
    Insert symbols to Mysql
    '''
    
    db_host = 'localhost'
    db_user = 'clz'
    db_pass = '1'
    db_name = 'stock'

    con = mdb.connect(
        host=db_host, user=db_user, passwd=db_pass, db=db_name
    )

    # Create the insert strings
    column_str = """stockname, stockid, stockdate, iflasheng"""

    insert_str = ("%s, " * 4)[:-2]
    final_str = "INSERT INTO lasheng (%s) VALUES (%s)" % \
        (column_str, insert_str)

    # Using the MySQL connection, carry out 
    # an INSERT INTO for every symbol
    with con: 
        cur = con.cursor()
        try:
            cur.executemany(final_str, symbols)
        except Exception as e:
            print("[ERROR] {}".format(e))




def main():
    date = getYesterday()
    symbols = stockLasheng(date = date)
    intoDB(symbols)


def getMysqlForWeb():
    '''
    get data from mysql
    :param date: 
    :return: 
    '''
    db_host = 'localhost'
    db_user = 'clz'
    db_pass = '1'
    db_name = 'stock'

    con = mdb.connect(
        host=db_host, user=db_user, passwd=db_pass, db=db_name
    )

    date = getYesterday()
    sqlStr ="select 1 from stock.lasheng where " \
            "stockdate ='{}'".format(date)
    check = pd.read_sql(sqlStr, con)
    if check.shape[0] == 0 :
        # request yesterday
        print("[info] get request data {}".format(date))
        main()

    beforedate = datetime.datetime.strptime(date,"%Y-%m-%d") - datetime.timedelta(days=7)
    sqlStr ="select stockname, stockid, stockdate, iflasheng " \
            "from stock.lasheng " \
            "where stockdate > '{}' and stockdate <='{}'".format(beforedate,date)
    print(sqlStr)

    getData = pd.read_sql(sqlStr, con)
    dataJsonRecord = getData.to_json(orient="records")

    return dataJsonRecord

if __name__ == "__main__":
    getMysqlForWeb()
