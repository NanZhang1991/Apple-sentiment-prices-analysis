# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 11:07:23 2020

@author: YJ001
"""
import os 
import numpy as np
import pandas as pd 
import datetime
from app.text_process.text_process import language_category, seg_words, timer
from app.sentiments_analysis.sentiments import run_score, emotion_words, Media_category
from app.sql_connect.sql_connect import get_data_from_sql, find_add_data, del_error_data, to_database
import schedule
from app.sentiments_analysis.sentiment_report import Parameter
from app.sentiments_analysis.Early_warning import  pre_warning
import time
from app.TRlogger import logger

log = logger('app/log_output/text_pre_pro.log','sentiment_analyse.py')

def data_pre_process(df):
    df.dropna(subset=['content'],inplace=True)
    df = df[df['content'].str.contains('[a-zA-Z]|[\u4e00-\u9fa5]{5}')]
    return df

def del_error_text(df, table_name):
    df['language'] = df['content'].apply(language_category)
    df_error = df[df['language']=='']
    # df_error.to_excel('test/sentiment_test/sentiment_data_source/output/'+ str(time.time())+'error.xlsx')
    if df_error.empty == False:
        error_id_tup = tuple(df_error['id'].tolist())
        del_error_data(table_name, error_id_tup)
    df = df[df['language'].isin(["Chinese","English"])]
    return df

@timer('文本预处理所花费时间为',log)
def main(df):   
    df = data_pre_process(df)
    df['Media_category'] = df['source'].apply(Media_category) 
    df = seg_words(df)
    df = run_score(df)  
    df = emotion_words(df)
    if "Amount_of_forward" not in df.columns:
        df["Amount_of_forward"] = np.nan
        df["Number_of_Fans"] = np.nan
        df["Big_V_type"] = ''
        
    df = df[["id","title","content","typename","source","pubtime","createtime","seg_words","detailurl",
             "score","Machine_emotion_lable","poswords","negwords","Media_category","Amount_of_forward","Number_of_Fans","Big_V_type"]]
    return df
 
class Scheduled_task:
    @staticmethod
    def sentiments_process(table_name, seg_table_name):
        try: 
            t1 = time.time()         
            df = find_add_data(table_name, seg_table_name)
            t2 = time.time()
            cost_time = t2-t1  
            df = del_error_text(df, table_name)       
            if df.empty != True:
                log.info(f'数据查询所花费时间为{cost_time}') 
                log.info("原始表{}，{}至{}期间添加的原始文本".format(table_name,df.createtime.tolist()[-1], df.createtime.tolist()[0]))
                after_df = main(df)
                # after_df.to_excel('test/sentiment_test/sentiment_data_source/output/'+ seg_table_name +'5.xlsx')
                to_database(after_df, seg_table_name)
                log.info("原始文本处理完成，存入数据库表{}".format(seg_table_name))
            else:
                # log.info("没有新增数据") 
                pass
        except Exception as e:
            error_line = e.__traceback__.tb_lineno
            log.info(f'第{error_line}行发生error为: {e}')  

    @staticmethod
    def run(table_name, seg_table_name):
        schedule.every(10).minutes.do(Scheduled_task.sentiments_process, table_name, seg_table_name)
        while 1:
            try:
                schedule.run_pending()  
            except Exception as e:
                error_line = e.__traceback__.tb_lineno
                log.info(f'第{error_line}行发生error为: {e}')


def sentiment_report(df, start, end):
     parameter = Parameter(df, start, end)
     total_dict = {}
     total_dict['全部声浪最高'] = parameter.total_tendency_rank.loc[0:0,['监测时间','全部声浪']].to_dict(orient='list')
     total_dict['重要媒体声浪最高'] = parameter.total_tendency_vip_rank.loc[0:0,['监测时间','重要媒体声浪']].to_dict(orient='list')
     total_dict['整体趋势'] = parameter.total_tendency_df.to_dict(orient='list')
     total_dict['内容分析'] = parameter.content_total()
     total_dict['倾向性趋势'] = parameter.tend_tendency_df.to_dict(orient='list')
     total_dict['倾向性分布'] = parameter.total_rate_df.to_dict(orient='index')
     total_dict['热词词云'] = parameter.words_tf_idf_dict     
     total_dict['媒体分析'] = parameter.Media_content_dict
     total_dict['媒体趋势'] = parameter.Media_tendency_df.to_dict(orient='list')
     total_dict['媒体对比'] = parameter.Media_count_df.to_dict(orient='list')
     total_dict['媒体分布'] = parameter.Media_distribution_df.to_dict(orient='list')
     total_dict['活跃媒体'] = parameter.hot_Media_df.to_dict(orient='list')
     if not parameter.weibo_df.empty:
          total_dict['微博趋势'] = parameter.weibo_tend_df.to_dict(orient='list')
          total_dict['微博倾向性分布'] = parameter.weibo_rate_df.to_dict(orient='list')
          total_dict['微博热词词云'] = parameter.weibo_words_tfidf_dict
          total_dict['微博热词统计'] = parameter.weibo_words_tf_dict     
          total_dict['大V类型'] = parameter.weibo_big_v_count_df.to_dict(orient='list')
          total_dict['粉丝数量'] = parameter.fans_amount_df.to_dict(orient='list')  
     return total_dict

def sentiments_pre_warning(df, start, end):
     parameter = Parameter(df, start, end)
     warning_df, weibo_warning_df = pre_warning(df, parameter)
     total_dict = {}
     total_dict['总体'] = warning_df.to_dict(orient='list')
     if not weibo_warning_df.empty:
        total_dict['微博'] = weibo_warning_df.to_dict(orient='list')     
     return total_dict

if __name__ == '__main__':
    table_name = "search_apple_news"
    new_table_name = 'seg' + '_' + table_name
    start = '2020-06-30 11:25:00'
    end = '2020-06-23 14:34:00'    
    sql_cmd ='''select * from {} where pubtime between "{}" and "{}" '''.format(table_name, start, end)  
    df = get_data_from_sql(sql_cmd)
    
    try:
        if df.empty == True:
           raise Exception("没有数据")
    except Exception as e:
        print(e)
        
    df_after = main(df)
    to_database(df_after, new_table_name)
    
  
    