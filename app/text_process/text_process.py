# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 09:59:52 2020

@author: YJ001
"""
import numpy as np
import pandas as pd
from langdetect import detect
import re 
import os 
from zhon.hanzi import punctuation
from nltk.corpus import stopwords 
from nltk import tokenize  
from nltk.tokenize import word_tokenize
import string
import jieba 
from sklearn.cluster import DBSCAN
from sklearn.decomposition import LatentDirichletAllocation
import collections
import itertools
from sklearn.feature_extraction.text import CountVectorizer  
from sklearn.feature_extraction.text import TfidfTransformer
Count_vectorizer = CountVectorizer()
transformer = TfidfTransformer() 
from app.TRlogger import logger
import warnings
import time
warnings.filterwarnings("ignore")
log = logger('app/log_output/text_pre_pro.log','text_process')

def timer(message,log):
    def wrapper(func):
        def insert_message(*args, **kwargs):
            t1= time.time()
            result = func(*args, **kwargs)
            t2 =time.time()
            cost_time = t2-t1
            log.info(f"函数{func.__name__}， {message} 花费时间：{cost_time}秒")
            return result
        return insert_message
    return wrapper

def cn_cut_sentence(text):
    sentence_list = re.split(r'(\.|\!|\?|。|！|？|\.{6})', text)
    return sentence_list

def cn_tokenize(sentence):
    seg_list = jieba.cut(sentence)
    return ",".join(seg_list).split(",")

# 中文情感程度副词       
def cn_weighted_words():
    cn_weighted_value = pd.read_excel('app/NLP_source/情感极性词典.xlsx')
    cn_mostdict = cn_weighted_value['cn_mostdict'].dropna()
    cn_verydict = cn_weighted_value['cn_verydict'].dropna()
    cn_moredict = cn_weighted_value['cn_moredict'].dropna()
    cn_ishdict = cn_weighted_value['cn_ishdict'].dropna()
    cn_insufficientdict = cn_weighted_value['cn_insufficientdict'].dropna()
    cn_inversedict = cn_weighted_value['cn_inversedict'].dropna()
    cn_weighted_words_list = list(itertools.chain(cn_mostdict, cn_verydict, cn_moredict, cn_ishdict, cn_ishdict, cn_insufficientdict, cn_inversedict))
    return cn_weighted_words_list


cn_stop_words = pd.read_excel("app/NLP_source/stopwords/cn_stopwords.xlsx")
cnbd_stopwords = cn_stop_words['baidu_stopwords']    
# 从停用词中去除程度副词
Cw_s_d = set(cnbd_stopwords) - set(cn_weighted_words())
def cn_del_stopwords(word_list):
     # 去除停用词后的句子   
    new_words = [word for word in word_list if word not in Cw_s_d ]
    return new_words


def cn_text_process(text_sent):   
    #对文章进行分句
    new_text_sent =""
    sentence_list = cn_cut_sentence(text_sent.replace('\n',''))
    for sent in sentence_list:
        word_list = cn_tokenize(sent)
        seg_words = cn_del_stopwords(word_list)  
        ren_words = remove_numbers(seg_words)
        rep_words = remove_punctuation(ren_words) 
        new_words = " ".join(rep_words)        
        if new_words !='':
            new_text_sent += new_words + " "   
    return new_text_sent.strip()

#去除文本中的数字 (主要针对分词后的英文，分词后的中文不存在)
def remove_numbers(words_list): 
    renum_words = [word for word in words_list if not word.isnumeric()]
    new_words = [word for word in renum_words if not re.findall('-\d+',word)]
    return new_words

#去除中英文标点符号
def remove_punctuation(words_list):
    new_words = [word for word in words_list if word not in punctuation and word not in string.punctuation]
    return new_words


def en_read_file(file_path):
    with open(file_path, 'r')as f:
        text = f.read()
        #返回list类型数据
        text = text.split('\n')
        text = [txt.strip() for txt in text]
    return text

def en_write_data(file_path, data):
    with open(file_path,'a+')as f:
        f.write(str(data))

# 英文情感程度副词        
def en_weighted_words():
    en_weighted_value = pd.read_excel(r'app/NLP_source/sentiment.xlsx')
    en_mostdict = en_weighted_value['most'].str.strip().dropna()
    en_verydict = en_weighted_value['very'].str.strip().dropna()
    en_moredict = en_weighted_value['more'].str.strip().dropna()
    en_ishdict = en_weighted_value['ish'].str.strip().dropna()
    en_insufficientdict = en_weighted_value['insufficiently'].str.strip().dropna()
    en_inversedict = en_weighted_value['inverse'].str.strip().dropna()
    en_weighted_words_list = list(itertools.chain(en_mostdict, en_verydict, en_moredict, en_ishdict, en_ishdict, en_insufficientdict, en_inversedict))
    return en_weighted_words_list

#英文去停用词函数
Ew_s_d = set(stopwords.words('english')) - set(en_weighted_words())
def en_del_stopwords(words_list):
    # 去除停用词后的句子
    new_words = [word for word in words_list if word not in Ew_s_d]
    return new_words

def en_text_process(text_sent):   
    #对文章进行分句
    new_text_sent = ""
    sentence_list = tokenize.sent_tokenize(text_sent.replace('\n',''))
    for sent in sentence_list:
        word_list = word_tokenize(sent)
        seg_words =en_del_stopwords(word_list)
        ren_words = remove_numbers(seg_words)
        rep_words = remove_punctuation(ren_words) 
        new_words = " ".join(rep_words)
        if new_words !='':
            new_text_sent += new_words + " "  
    return new_text_sent.strip()

def language_category(text_sent):
    try:
        language = detect(text_sent)
        if language == 'zh-cn':
            result = "Chinese"
        elif language =='en':
            result = "English"
        else:
            result =''
    except Exception as e:
        error_line = e.__traceback__.tb_lineno
        log.info(f'第{error_line}行发生error为: {e} #### {text_sent}识别为空的字符串')
        result = ''
    return result  

def seg_words(df):
    df['seg_words'] = ''
    # print("process Chinese text...")
    df['seg_words'][df['language']=="Chinese"] = df['content'][df['language']=="Chinese"].apply(cn_text_process)
    # print("process English text...")
    df['seg_words'][df['language']=="English"] = df['content'][df['language']=="English"].apply(en_text_process)
    return df
