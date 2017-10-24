#!encoding=utf-8
import tushare as ts
import MySQLdb as mdb
from sqlalchemy import create_engine


def getHangye():
    '''
    获取行业信息
    :return: 
    '''
    hangyeData = ts.get_industry_classified()
    #hangyeData.to_csv("../../data/hangyeData.csv")
    return hangyeData


def getGainian():
    '''
    获取概念
    :return: 
    '''
    gainian = ts.get_concept_classified()
    #gainian.to_csv("../../data/gainianData.csv")
    #print gainian
    return gainian


def bankuaiIntoDB():
    '''
    into DB
    :return: 
    '''
    db_host = 'localhost'
    db_user = 'clz'
    db_pass = '1'
    db_name = 'stock'

    con = mdb.connect(
        host=db_host, user = db_user, passwd = db_pass, db = db_name
    )


    engine = create_engine('mysql://clz:1@127.0.0.1/stock?charset=utf8')
    cur = con.cursor()

    dropStr = "delete from stock.hangyeinfo"
    print("[INFO] begin to get hangye")
    try:
        hangyeData = getHangye()
        cur.executemany(dropStr,"")
        hangyeData.to_sql('hangyeinfo', engine)

    except Exception as e:

        print ("[ERROR] {}".format(e))


    dropStr = "delete from stock.gainianinfo"
    print("[INFO] begin to get gainian")
    try:
        gainianData = getGainian()
        cur.executemany(dropStr,"")
        gainianData.to_sql('gainianinfo', engine)

    except Exception as e:

        print ("[ERROR] {}".format(e))




if __name__ == "__main__":
    bankuaiIntoDB()



