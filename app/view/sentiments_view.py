from . import sentiments
from flask import render_template, request, jsonify
from app.sentiments_analysis.sentiment_analyse import Scheduled_task, sentiment_report, sentiments_pre_warning
from app.sql_connect.sql_connect import get_data_from_sql, to_database
import pandas as pd
import os
import json
import datetime
from app.TRlogger import logger
import schedule
import datetime
from dateutil.relativedelta import relativedelta
log = logger('app/log_output/run.log','sentiments_view.py')

@sentiments.route("/test", methods=['POST'])     
def test():
    return 'Hello world'

@sentiments.route("/select_report", methods=['POST'])
def get_sentiments_report():
     try:
          start = request.form.get('start') 
          end = request.form.get('end')  
          # print( "前端传入的数据", request.form,type(start),start, type(end),end )         
          table_name = "2020_seg_sentiment_content"
          # test_data
          # df = pd.read_excel(os.path.join(os.getcwd(), 'test/sentiment_test/sentiment_data_source/input/seg_tea_hotspot.xlsx'))
          sql_cmd ='''select * from {} where pubtime between "{}" and "{}" and source !="烟台市人民政府" '''.format(table_name, start, end)  
          df = get_data_from_sql(sql_cmd)
          if not df.empty:
               result = sentiment_report(df, start, end)
          else:
               result = None
          # with open(r'test\sentiment_test\sentiment_data_source\output\sentiment_report.json', 'w') as f: 
          #      json.dump(result, f, indent=2, ensure_ascii=False)
     except Exception as e:
        error_line = e.__traceback__.tb_lineno
        log.info(f'第{error_line}行发生error为: {e}')      
        result = f'第{error_line}行发生error为: {e}'    
     return jsonify(result)


@sentiments.route("/report", methods=['POST'])
def get_per_month_report():   
     with open('app/result/per_month_report.json','r') as f: 
          result = json.load(f)
     return jsonify(result)




