# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 11:06:17 2020

@author: YJ001
"""

import pandas as pd


class Price_index():
    
    def __init__(self, df):
        self.df = self.pre_process(df)

    def pre_process(self, df):
        if 'AVG_PRICE' not in df.columns:
            df['AVG_PRICE'] = (df.MIN_PRICE + df.MAX_PRICE)/2
        df = df.drop(df[df['AVG_PRICE']==0].index)
        df['date'] = df.CREATE_DATE.apply(lambda x : x.date())
        return df     
    
    def get_pri_i(self):
        df_variety_p = self.df.pivot_table(values='AVG_PRICE', index='date', columns ='VARIETY', aggfunc='mean')
        df_variety_p['AVG_PRICE'] = df_variety_p.mean(1)
        s_price = df_variety_p['AVG_PRICE'].sort_index()
        s_price_i= (s_price - s_price.shift(1)) / s_price.shift(1)
        s_price_i = s_price_i.fillna(0).apply(lambda f: '%.2f' % (f*100))
        df_price_i = s_price_i.reset_index()
        df_price_i.date = df_price_i.date.astype(str)
        return df_price_i
    
    def get_varietys(self):
        df_variety_p = self.df.pivot_table(values='AVG_PRICE', index='date', columns ='VARIETY', aggfunc='mean')
        dict_from_variety_p={}
        for variety in df_variety_p.columns:
            dict_from_variety_p[variety] = df_variety_p[variety].count()   
        s_variety_p = pd.Series(dict_from_variety_p).sort_values(ascending=False).head()
        df_variety_pp = df_variety_p[s_variety_p.index].sort_index()
        varietys = df_variety_pp.columns.tolist()
        return varietys
    
    def variety_pi(self, column):
        df_variety_p = self.df.pivot_table(values='AVG_PRICE', index='date', columns ='VARIETY', aggfunc='mean')
        dict_from_variety_p={}
        for variety in df_variety_p.columns:
            dict_from_variety_p[variety] = df_variety_p[variety].count()   
        s_variety_p = pd.Series(dict_from_variety_p).sort_values(ascending=False).head()
        df_variety_pp = df_variety_p[s_variety_p.index].sort_index()
        singe_variety_p = df_variety_pp[column].dropna()
        singe_variety_p_i = (singe_variety_p - singe_variety_p.shift(1)) / singe_variety_p.shift(1)
        singe_variety_p_i = singe_variety_p_i.fillna(0).apply(lambda f: '%.2f' % (f*100))
        df_svpi = singe_variety_p_i.reset_index()
        df_svpi.date = df_svpi.date.astype(str)
        return  df_svpi

'''
指数的计算公式。
价格指数的计算公式以派氏公式I=∑P1Q1/∑P0Q1和
拉氏公式I=∑P1Q0/∑P0Q0为基本公式。但在实际工作中往往根据所掌握资料的情况,分别采用变形公式,
即加权调和公式,也称加权倒数公式I=∑P1Q1/(∑(P1Q1)/k)和加权算术平均公式I=∑kP0Q0/∑P0Q0。
'''
if __name__=="__main__":
    df = pd.read_excel('C:/Users/YJ001/Desktop/project/Yantai_apple_analysis/test/peice_index/a_price.xlsx')


    pi = Price_index(df)
    df_price_i = pi.get_pri_i()
    columns = pi.get_varietys() 
    column = '富士'
    df_svpi = pi.variety_pi(column)


    





