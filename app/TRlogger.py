# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 13:11:24 2020

@author: YJ001
"""

import logging
from logging import handlers 

def logger(filename, module_name):
    logging.basicConfig()
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)    
    th = handlers.TimedRotatingFileHandler(filename=filename, when="MIDNIGHT", interval=1, backupCount=3, encoding='utf-8')
    th.suffix = "%Y-%m-%d.log"
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    th.setFormatter(formatter)
    th.setLevel(logging.DEBUG)
    logger.addHandler(th)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.removeHandler(stream_handler)
    return logger


if __name__ == "__main__":
    logger = logger('app/log_output/my.log', __name__)
    

    logger.debug('Quick zephyrs blow, vexing daft Jim.')
    logger.info('How quickly daft jumping zebras vex.')
    logger.error('unknow')
    import os 
    import sys
    print(os.path.basename(sys.argv[0]))