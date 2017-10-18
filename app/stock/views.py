# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify
from . import stock
from .utils import getStock,getLonghuNew

@stock.route( "/get_kchart", methods = [ "POST", "GET" ] )
def get_kchart():

    if request.method == "POST":
        stockname = request.form.get( "stockId", "null" )
        stockData = getStock(stockname)
        datas = {
            "stockname" : stockname,
            "stockData" : stockData
        }

        return jsonify(datas)
    else:
        return render_template("stock/get_kchart.html")


@stock.route( "/get_longhu_new", methods = [ "POST", "GET" ] )
def get_longhu_new():

    if request.method == "POST":
        getDate = request.form.get("getDate", "null" )

        longhuData = getLonghuNew(getDate)
        datas = {
            "name": u"龙虎榜",
            "longhu" : longhuData,
        }

        return jsonify(datas)

    else:
        return render_template("stock/get_longhu_new.html")

@stock.route("/lab")
def lab():
    return render_template("stock/lab.html")
