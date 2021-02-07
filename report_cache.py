
from app.TRlogger import logger
import schedule
import datetime
from dateutil.relativedelta import relativedelta
from app.sql_connect.sql_connect import get_data_from_sql
from app.sentiments_analysis.sentiment_analyse import  sentiment_report
import json
import os 
import sys

log = logger('app/log_output/report_cache.log','report_cache.py')

def get_report_cache():
    log.info('get_report_cache')
    schedule.every().hours.do(per_month_report)
    while 1:
        try:
            schedule.run_pending()  
        except Exception as e:
            error_line = e.__traceback__.tb_lineno
            log.info(f'第{error_line}行发生error为: {e}')
    
def per_month_report():  
    try:
        now = datetime.datetime.now()
        start = (now - relativedelta(months=1)).strftime("%Y-%m-%d %H:%M:%S")
        end = now.strftime("%Y-%m-%d %H:%M:%S")
        table_name = "2020_seg_sentiment_content"
        sql_cmd ='''select * from {} where pubtime between "{}" and "{}" '''.format(table_name, start, end)  
        df = get_data_from_sql(sql_cmd)
        if not df.empty:
            df.sort_values('pubtime', inplace=True, ascending=False)
            df.reset_index(drop=True,inplace=True)
            result = sentiment_report(df, start, end)
            with open('app/result/per_month_report.json', 'w') as f: 
                json.dump(result, f, indent=2, ensure_ascii=False)
                log.info(f"{df.loc[0,'pubtime']} 时间前的数据已更新")
        else:
            result = None
    except Exception as e:
        error_line = e.__traceback__.tb_lineno
        log.info(f'第{error_line}行发生error为: {e}')
get_report_cache()