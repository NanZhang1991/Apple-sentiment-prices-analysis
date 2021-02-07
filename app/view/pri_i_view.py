# -*- coding: utf-8 -*-
from . import price_index
from flask import render_template, request, jsonify
from app.sql_connect.sql_connect import get_data_from_sql
from app.price_index.price_index import Price_index

@price_index.route('/')
def hello_world():
    return 'Hello World!'

@price_index.route('get_pri_i/<kind>', methods=['POST'])
def get_pri_i(kind):
    start_date = request.form.get('start') 
    end_date = request.form.get('end')    
    # start_date = "2020-1-20"
    # end_date = "2020-7-14"
    if kind == 'retail':
        sql_cmd = "SELECT a.TYPE, a.CREATE_DATE, b.* FROM bd_fruit_price a RIGHT join  bd_fruit_price_detail b ON a.ID=b.PRICE_ID WHERE a.TYPE = 'market' \
        and CREATE_DATE between '{}' AND '{}'".format(start_date, end_date)
    elif kind == 'from':       
        sql_cmd = "SELECT a.TYPE,a.CREATE_DATE, b.* FROM bd_fruit_price a RIGHT join  bd_fruit_price_detail b ON a.ID=b.PRICE_ID WHERE a.TYPE = 'from'\
        and CREATE_DATE between '{}' AND '{}'".format(start_date, end_date)  
    elif kind == 'market':
        sql_cmd = "SELECT * FROM abd_market_price WHERE TYPE = 'market' \
                  and CREATE_DATE between '{}' AND '{}'".format(start_date, end_date)
        
    df = get_data_from_sql(sql_cmd)
    if df.empty == False:
        # print(df.head())
        pi = Price_index(df)
        df_price_i = pi.get_pri_i()
        # print(df_price_i.head())
        df_price_i.rename(columns={df_price_i.iloc[:,1].name:'pi'}, inplace=True)
        result = df_price_i.to_dict() 
    else:
        result = None   
    return jsonify(result)

@price_index.route('varietys/<kind>', methods=['POST'])
def get_varietys(kind):
    start_date = request.form.get('start') 
    end_date = request.form.get('end') 
    if kind == 'retail':
        sql_cmd = "SELECT a.TYPE, a.CREATE_DATE, b.* FROM bd_fruit_price a RIGHT join  bd_fruit_price_detail b ON a.ID=b.PRICE_ID WHERE a.TYPE = 'market' \
        and CREATE_DATE between '{}' AND '{}'".format(start_date, end_date)
    elif kind == 'from':       
        sql_cmd = "SELECT a.TYPE,a.CREATE_DATE, b.* FROM bd_fruit_price a RIGHT join  bd_fruit_price_detail b ON a.ID=b.PRICE_ID WHERE a.TYPE = 'from'\
        and CREATE_DATE between '{}' AND '{}'".format(start_date, end_date)  
    elif kind == 'market':
        sql_cmd = "SELECT * FROM abd_market_price WHERE TYPE = 'market' \
                  and CREATE_DATE between '{}' AND '{}'".format(start_date, end_date)     
    df = get_data_from_sql(sql_cmd)
    if df.empty == False:
        pi = Price_index(df)
        varietys = pi.get_varietys()
        # print(varietys[:5])
        result = varietys
    else:
        result = None
    return jsonify(result)

@price_index.route('svpi/<kind>', methods=['POST'])
def df_variety_p(kind):
    start_date = request.form.get('start') 
    end_date = request.form.get('end') 
    variety = request.form.get('variety')
    if kind == 'retail':
        sql_cmd = "SELECT a.TYPE, a.CREATE_DATE, b.* FROM bd_fruit_price a RIGHT join  bd_fruit_price_detail b ON a.ID=b.PRICE_ID WHERE a.TYPE = 'market' \
        and CREATE_DATE between '{}' AND '{}'".format(start_date, end_date)
    elif kind == 'from':       
        sql_cmd = "SELECT a.TYPE,a.CREATE_DATE, b.* FROM bd_fruit_price a RIGHT join  bd_fruit_price_detail b ON a.ID=b.PRICE_ID WHERE a.TYPE = 'from'\
        and CREATE_DATE between '{}' AND '{}'".format(start_date, end_date)  
    elif kind == 'market':
        sql_cmd = "SELECT * FROM abd_market_price WHERE TYPE = 'market' \
                  and CREATE_DATE between '{}' AND '{}'".format(start_date, end_date)
        
    df = get_data_from_sql(sql_cmd)
    if df.empty == False:
        pi = Price_index(df)
        df_svpi = pi.variety_pi(variety)
        # print(df_svpi.head())
        df_svpi.rename(columns={df_svpi.iloc[:,1].name:'svpi'}, inplace=True)
        result = df_svpi.to_dict()
    else:
        result = None
    return jsonify(result)
