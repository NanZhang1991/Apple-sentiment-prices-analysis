# -*- coding: utf-8 -*-

import pandas as pd 
import sqlalchemy 
from sqlalchemy import create_engine
import pymysql
import re 

def table_exists(table_name):
    connect = pymysql.connect(host="127.0.0.1",
                              user="root",
                              password="1234",
                              port=3306,                   
                              db ="yt_apple_bigdata",
                              charset = 'utf8')   
    con = connect.cursor()    
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    if table_name in table_list:
        return 1
    else:
        return 0

def find_add_data(table_name, seg_table_name):
    DB_USER = "root"
    DB_PASS = 1234"
    DB_HOST =  "127.0.0.1"
    DB_PORT = "3306"
    DATABASE = "yt_apple_bigdata"
    connect_info = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE)
    engine = create_engine(connect_info, pool_size=100)   
    # # 去除重复数据 
    # sql_del_dup = f"DELETE from {table_name} where ID not in (select Mid from (select Max(id) Mid from {table_name} group by content) temp_c)"
    # con_dup = engine.execute(sql_del_dup)
    # con_dup.close() 

    sql_find_add = f'''select * from {table_name} where id not in (select id from {seg_table_name}) and date_sub(CURRENT_DATE(), interval 1 month) <=date(pubtime) ORDER BY pubtime desc limit 1000'''
    df = pd.read_sql(sql_find_add, con=engine)
    return df 
    
def get_data_from_sql(sql_cmd):
    DB_USER = "root"
    DB_PASS = "1234"
    DB_HOST =  "127.0.0.1"
    DB_PORT = "3306"
    DATABASE = "yt_apple_bigdata"
    connect_info = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE)
    engine = create_engine(connect_info)

    df = pd.read_sql(sql_cmd, con=engine)
    return df 
    
def del_error_data(table_name, error_id_tup):
    DB_USER = "root"
    DB_PASS = "1234"
    DB_HOST =  "127.0.0.1"
    DB_PORT = "3306"
    DATABASE = "spider_data"
    connect_info = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE)
    engine = create_engine(connect_info, pool_size=100)
    sql_del_error = f'''delete from {table_name} where id in {error_id_tup}'''
    con_error = engine.execute(sql_del_error)
    con_error.close() 

def to_database(df, table_name): 
    DB_USER = "root"
    DB_PASS = "1234"
    DB_HOST =  "127.0.0.1"
    DB_PORT = "3306"
    DATABASE = "yt_apple_bigdata"
    connect_info = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE)
    engine = create_engine(connect_info)

    # 写入数据库
    df.to_sql(name=table_name, con=engine, if_exists='append',
              index=False, dtype={"ID":sqlalchemy.Text(),"title":sqlalchemy.Text(), "content":sqlalchemy.Text(),
                                  "typename":sqlalchemy.Text(), "source":sqlalchemy.Text(),
                                  "pubtime": sqlalchemy.DateTime(), "createtime":sqlalchemy.DateTime(),                                  
                                  "detailurl":sqlalchemy.Text(),"seg_words":sqlalchemy.Text(), 
                                  "Media_category":sqlalchemy.Text(), 
                                  "score":sqlalchemy.Text(), "Machine_emotion_lable":sqlalchemy.Text(),
                                  "poswords":sqlalchemy.Text(), "negwords":sqlalchemy.Text(),
                                  "Amount_of_forward":sqlalchemy.types.INTEGER(),
                                  "Number_of_Fans":sqlalchemy.types.INTEGER(),
                                  "Big_V_type":sqlalchemy.Text()})

    
