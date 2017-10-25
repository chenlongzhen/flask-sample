#encoding=utf-8
# 股票涨停日

import tushare as ts
import datetime
import MySQLdb as mdb
from sqlalchemy import create_engine
import pandas as pd

from app.stock.utils import getYesterday


def intoDB(date='2017-10-20'):
    '''
    Insert symbols to Mysql
    ''' 
    print("[info] getting {}".format(date))
    data = ts.top_list(date)
    data['date'] = date
    data = data.drop_duplicates(['code','date'])

    print("[info] into mysql")
    engine = create_engine('mysql://clz:1@127.0.0.1/stock?charset=utf8', encoding='utf-8')

    try:
        data.to_sql('longhu', engine, if_exists = "append", index=False)
    except Exception as e:
        print("error: {}".format(e))

def longhuMain():
    date = getYesterday()
    intoDB(date)


def longHuGetMysqlForWeb():
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
        host=db_host, user=db_user, passwd=db_pass, db=db_name,charset="utf8"
    )

    date = getYesterday()

#    check and getdata
#    sqlStr ="select 1 from stock.longhu where " \
#            "date ='{}'".format(date)
#    check = pd.read_sql(sqlStr, con)
#    if check.shape[0] == 0 :
#        # request yesterday
#        print("[info] get request data {}".format(date))
#        longhuMain()

    beforedate = datetime.datetime.strptime(date,"%Y-%m-%d") - datetime.timedelta(days=7)
    sqlStr ="select code, name, pchange, amount, buy, sell,reason,bratio,sratio,date_format(date,'%Y-%c-%d') as sdate " \
            "from stock.longhu " \
            "where date > '{}' and date <='{}' order by date desc ,pchange desc".format(beforedate,date)
    print(sqlStr)

    getData = pd.read_sql(sqlStr, con)
    #print(getData) 
    dataJsonRecord = getData.to_json(orient="records")
    #print dataJsonRecord
    return dataJsonRecord

if __name__ == "__main__":
    longHuGetMysqlForWeb()
