# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:14:01 2020

@author: YJ001
"""
import os
import pandas as pd 
from nltk.corpus import stopwords 
from sklearn.feature_extraction.text import CountVectorizer  
from sklearn.feature_extraction.text import TfidfTransformer
import collections


en_stop_words = list(set(stopwords.words('english')))
cn_stop_words =  pd.read_excel("app/NLP_source/stopwords/cn_stopwords.xlsx")
cnbd_stop_words = list(cn_stop_words['baidu_stopwords']) 
stop_words = en_stop_words + cnbd_stop_words


def calculate_tf(corpus):
    vectorizer = CountVectorizer(stop_words=stop_words, max_features=20) 
    X = vectorizer.fit_transform(corpus)  
    words = vectorizer.get_feature_names()   
    df_word_tf = pd.DataFrame(X.toarray(),columns=words) 
    word_tf_sum = df_word_tf.sum().sort_values(ascending=False)
    return  word_tf_sum
    
    
def calculate_tfidf(corpus):    
    vectorizer = CountVectorizer(stop_words=stop_words, max_features=20)    
    X = vectorizer.fit_transform(corpus)  
    words = vectorizer.get_feature_names()   
    transformer = TfidfTransformer()  
    tfidf = transformer.fit_transform(X)  
    df_wordFreq = pd.DataFrame(tfidf.toarray(),columns=words) 
    wordFreqSum = df_wordFreq.sum().sort_values(ascending=False) #计算每个特征的总词频并按照降序进行排序
    return wordFreqSum


if __name__ == '__main__':
    print('Processing........')

    corpus = [  
        'This is the first document.',  
        'This is the second second document.',  
        'And the third one.',  
        'Is this the first document?',  
    ]  

    tf = calculate_tf(corpus)
    tf_idf = calculate_tfidf(corpus)
    print('finish...')

