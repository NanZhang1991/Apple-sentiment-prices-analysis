
from app.sentiments_analysis.sentiment_analyse import Scheduled_task
import pandas as pd
import datetime
from app.TRlogger import logger
import os 
import sys

log = logger('app/log_output/text_pre_pro.log',os.path.basename(sys.argv[0]))

def scheduled_task():
     table_name = 'search_apple_news'
     seg_table_name = '2020_seg_sentiment_content'
     log.info('search_apple_news')
     # 单个测试
     # Scheduled_task.sentiments_process(table_name, seg_table_name)
     Scheduled_task.run(table_name, seg_table_name)

scheduled_task()