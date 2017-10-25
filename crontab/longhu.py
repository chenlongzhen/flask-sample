#encoding=utf-8
# 股票涨停日

import tushare as ts
import datetime
import MySQLdb as mdb
from sqlalchemy import create_engine
import pandas as pd
from utils import *


def intoDB(date='2017-10-20'):
    '''
    Insert symbols to Mysql
    '''

    print("[info] getting {}".format(date))
    data = ts.top_list(date)
    data['date'] = date
    data = data.drop_duplicates(['code','date'])

    print("[info] into mysql")
    engine = create_engine('mysql://clz:1@127.0.0.1/stock?charset=utf8')

    try:
        data.to_sql('longhu', engine, if_exists = "append", index=False)
    except Exception as e:
        print("error: {}".format(e))


def longhuMain():
    date = getYesterday()
    intoDB(date)


def longHuIntoMysql():
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
    sqlStr ="select 1 from stock.longhu where " \
            "date ='{}'".format(date)
    check = pd.read_sql(sqlStr, con)
    if check.shape[0] == 0 :
        # request yesterday
        print("[info] get request data {}".format(date))
        longhuMain()
    else:
        print("[info] {} already in mysql".format(date))



if __name__ == "__main__":
    longHuIntoMysql()
