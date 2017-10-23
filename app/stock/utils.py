# coding=utf-8
import datetime
import tushare as ts
import pandas as pd
#top = ts.top_list('2017-06-12')
def getStock(name='sh'):
    '''
    GET STOCK HIST DATA
    :return: 
    '''
    # get stock data
    stock_data = ts.get_hist_data(name)[['open','close','low','high']]

    # sort by date
    stock_data.index = pd.to_datetime(stock_data.index)
    stock_data = stock_data.sort_index(axis=0, ascending=True)

    # process date
    #stock_data.index = map(lambda x: x.strftime('%Y-%m-%d'), stock_data.index)
    #dateData = map(lambda x: x.replace('-','/'),stock_data.index.tolist())
    stock_data['date'] = map(lambda x: x.strftime('%Y-%m-%d'), stock_data.index)
    stock_data['date'] = stock_data['date'].apply(lambda x: x.replace('-', '/'))
    stockData = stock_data[['date', 'open', 'close', 'low', 'high']]

    #histData = stock_data.values.tolist()
    #return dateData,histData
    return stockData.values.tolist()


def getLonghu(getDate = "2017-10-13"):
    '''
    获取机构成交明细
    :return: 
    '''
    data = ts.top_list(date = str(getDate))
    if data is None:
        return ['0'],['0']

    indexNameList = data.columns.values.tolist()
    dataList = data.values.tolist()

    return indexNameList,dataList

def getLonghuNew(getDate = "2017-10-13"):
    '''
    获取机构成交明细
    :return: 
    '''

    data = ts.top_list(date = str(getDate))

    if data is None:
        return ['0'],['0']

    dataJsonRecord = data.to_json(orient="records")



    #indexNameList = data.columns.values.tolist()
    #dataList = data.values.tolist()


    return dataJsonRecord

def getYesterday():

    sign = True
    print("[INFO] get yesterday...")
    date = datetime.datetime.now()
    yesterOneDay =  datetime.timedelta(days=-1)
    while sign:
        date += yesterOneDay
        print date
        print date.weekday()
        if date.weekday() >= 5:
            pass
        else:
            sign = False
    dataStr = date.strftime("%Y-%m-%d")
    print("[INFO] get date {}".format(dataStr))
    return dataStr

