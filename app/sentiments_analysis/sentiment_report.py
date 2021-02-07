# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 18:29:40 2020

@author: YJ001
"""

from app.sentiments_analysis.extract_keywords import calculate_tf, calculate_tfidf
import numpy as np
import pandas as pd
import json
import os 
import datetime
import random

def save_json(path, item):
    with open(path, "w", encoding='utf-8') as f:
        f.write(item + ",\n")
        print("^_^ write success")


class Parameter():
    def __init__(self, df, start, end):
        self.df = df
        self.weibo_df = self.df[self.df['Media_category']=='微博']
        self.start_datetime = datetime.datetime.strptime(start,'%Y-%m-%d %H:%M:%S')
        self.end_datetime =  datetime.datetime.strptime(end,'%Y-%m-%d %H:%M:%S')
        self.tendency_df = self.tendency()
        self.total_tendency_rank = self.total_tendency()[0].sort_values('全部声浪', ascending=False).reset_index()
        self.total_tendency_vip_rank = self.total_tendency()[0].sort_values('重要媒体声浪', ascending=False).reset_index() 
        self.total_tendency_df = self.total_tendency()[0]
        self.tend_tendency_df = self.total_tendency()[1]
        self.Media_tendency_df = self.total_tendency()[2]   
        self.rate_df = self.rate(self.df)  
        self.total_rate_df = self.total_rate() 
        self.words_tf_dict = self.words_tf()
        self.words_tf_idf_dict = self.words_tf_idf()[0]
        self.Media_count_df = self.Media_category_data()[0]
        self.Media_distribution_df = self.Media_category_data()[1]
        self.hot_Media_df = self.Media_category_data()[2]
        self.Media_content_dict = self.Media_content()
        self.poswords_tf_dict = self.poswords_tf_idf()[0]
        self.poswords_tfidf_dict = self.poswords_tf_idf()[1]
        self.negwords_tf_dict = self.negwords_tf_idf()[0]
        self.negwords_tfidf_dict = self.negwords_tf_idf()[1]
        if not self.weibo_df.empty:
            self.weibo_tend_df = self.weibo_tendency()
            self.weibo_rate_df = self.weibo_rate() 
            self.weibo_words_tf_dict = self.weibo_words_tf_idf()[0]
            self.weibo_words_tfidf_dict = self.weibo_words_tf_idf()[1]
            self.weibo_big_v_count_df = self.Big_V_type_count()
            self.fans_amount_df = self.Amount_of_fans()


    def tendency(self):
        self.df['time_quantum'] = self.df['pubtime'].apply(lambda x: datetime.datetime.strptime(str(x.year)+'-'+str(x.month)+'-'+str(x.day), '%Y-%m-%d'))
        '''
        time_delta = self.end_datetime - self.start_datetime
        if time_delta.days<=1:
            time_list =  [self.start_datetime + datetime.timedelta(hours=x*(time_delta.seconds/3600/10))
             for x in range(11)]
        else:
            time_list = [self.start_datetime + datetime.timedelta(days=x*(time_delta.days/10)) for x in range(11)]
        df_total = pd.DataFrame()
        for i in range(10):
            df_t = self.df[(self.df['pubtime']>=time_list[i]) & (self.df['pubtime']<time_list[i+1])][['Media_category','Machine_emotion_lable']]
            if df_t.empty:
                df_t.loc[0,'time_quantum'] = time_list[i+1]
            else:
                df_t['time_quantum'] = time_list[i+1]
            df_total = df_total.append(df_t)
        df_total.reset_index(drop=True, inplace=True)
        '''
        df_total = self.df[['time_quantum','Media_category','Machine_emotion_lable']]
        df_total = df_total.sort_values('time_quantum')
        return df_total
        
    def content_total(self):
        content_total = {}
        content_total['全部声浪最高'] = self.total_tendency_rank.loc[0,['监测时间','全部声浪']].to_dict()
        content_total['重要媒体声浪最高'] = self.total_tendency_vip_rank.loc[0,['监测时间','重要媒体声浪']].to_dict()
        content_total['共监测信息量'] = self.df.shape[0]
        content_total['最高负面信息'] = self.tend_tendency_df[['监测时间','消极']].sort_values('消极',ascending=False).head(1).max().to_dict()
        content_total['负面信息量'] = self.rate_df.loc[self.rate_df['类别'] =='负面','数据量'].tolist()[0]
        content_total['负面信息占比'] = self.rate_df.loc[self.rate_df['类别'] =='负面','占比'].apply(lambda f: '%.2f' % (f*100)+'%').tolist()[0]
        content_total['重点词语'] = "、".join(self.words_tf_idf()[1].index.tolist()[0:5])

        content_text={}
        content_text['概要趋势'] = '在整体发展趋势中，{}声量最高，共产生{}条信息。在{}重要媒体声量最高，共产生{}条信息。'.format(content_total['全部声浪最高']['监测时间'],\
                                   content_total['全部声浪最高']['全部声浪'], content_total['重要媒体声浪最高']['监测时间'], content_total['重要媒体声浪最高']['重要媒体声浪'] )
        # content_text['倾向性趋势'] = '{}负面信息最多，共{}条'.format(content_total['最高负面信息']['监测时间'],content_total['最高负面信息']['消极'])
        content_text['倾向性趋势'] = ""
        # content_text['倾向性分析'] = '在监测周期内，共监测到{}条信息，其中负面信息{}条，占比{}。'.format(content_total['共监测信息量'],content_total['负面信息量'], content_total['负面信息占比'])
        content_text['倾向性分析']  = '在监测周期内，共监测到{}条信息。'.format(content_total['共监测信息量'])
        content_text['热词词云'] = '在监测周期内媒体和网民主要关注与{}，相关的信息'.format( content_total['重点词语'])
        return content_text
        

    def total_tendency(self):
        time_quantum = pd.DataFrame({'监测时间':self.tendency_df['time_quantum'].unique()})

        total_voice_Ser = self.tendency_df.groupby('time_quantum')['Media_category'].count()
        # total_voice_Ser.sort_values(inplace=True) # 临时取升序
        # total_voice_Ser.index = time_quantum['监测时间'] # 临时取升序的索引

        impotant_Media_Ser = self.tendency_df[self.tendency_df['Media_category']=='政府或研究机构'].groupby('time_quantum')['Media_category'].count()
        # 增加随机值
        if impotant_Media_Ser.empty:
           impotant_Media_Ser = total_voice_Ser.apply(lambda x : x//10)
        #    impotant_Media_Ser.sort_values(inplace=True) # 临时取升序
        #    impotant_Media_Ser.index = time_quantum['监测时间'] # 临时取升序的索引
        # print(impotant_Media_Ser)

        total_tendency_df = pd.DataFrame({'全部声浪':total_voice_Ser, '重要媒体声浪':impotant_Media_Ser })
        total_tendency_df.index.rename('监测时间', inplace=True)
        total_tendency_df.reset_index(inplace=True)
        total_tendency_df.fillna(0,inplace=True) 
        total_tendency_df['监测时间'] = total_tendency_df['监测时间'].astype(str)
    
        tend_tendency_df = self.tendency_df.pivot_table(index='time_quantum',columns='Machine_emotion_lable',values='Media_category',aggfunc='count')
        tend_tendency_df.index.rename('监测时间', inplace=True)
        tend_tendency_df.reset_index(inplace=True)
        if '中性' not in tend_tendency_df.columns:
            tend_tendency_df['中性'] = np.nan
        if '积极' not in tend_tendency_df.columns:
            tend_tendency_df['积极'] = np.nan
        if '消极' not in tend_tendency_df.columns:
            tend_tendency_df['消极'] = np.nan     
        tend_tendency_df = pd.merge(time_quantum, tend_tendency_df, how='left', on='监测时间')
        tend_tendency_df['监测时间'] = tend_tendency_df['监测时间'].astype(str)
        tend_tendency_df.fillna(0,inplace=True)

        Media_tendency_df = self.tendency_df.pivot_table(index='time_quantum',columns='Media_category',values='Machine_emotion_lable',aggfunc='count')
        Media_tendency_df.index.rename('监测时间', inplace=True)
        Media_tendency_df.reset_index(inplace=True)   
        Media_tendency_df = pd.merge(time_quantum, Media_tendency_df, how='left', on='监测时间')
        Media_tendency_df['监测时间'] = Media_tendency_df['监测时间'].astype(str)
        Media_tendency_df.fillna(0,inplace=True)
        return  total_tendency_df, tend_tendency_df, Media_tendency_df

    def total_rate(self):
        total_rate_df = self.rate(self.df) 
        total_rate_df['占比'] = total_rate_df['占比'].apply(lambda f: '%.2f' % (f*100)+'%')
        return total_rate_df

    def rate(self, df):
        total = df['Machine_emotion_lable'].count()
        negtive_count = df['Machine_emotion_lable'][df['Machine_emotion_lable']=='消极'].count()
        postive_count = df['Machine_emotion_lable'][df['Machine_emotion_lable']=='积极'].count()
        neutral_count = df['Machine_emotion_lable'][df['Machine_emotion_lable']=='中性'].count()
        negtive_rate = negtive_count / total
        postive_rate = postive_count / total
        neutral_rate = neutral_count / total
        rate_df = pd.DataFrame({'类别':['正面','负面','中性'], '数据量':[postive_count, negtive_count, neutral_count],
                                '占比':[postive_rate, negtive_rate, neutral_rate]}).fillna(0)
        return rate_df

    def words_tf(self):
        words_tf_dict= calculate_tf(self.df['seg_words']).to_dict()     
        return  words_tf_dict

    def words_tf_idf(self):
        words_tfidf_df = calculate_tfidf(self.df['seg_words'])
        words_tfidf_df.sort_values(ascending=False, inplace=True)
        words_tf_idf_dict = words_tfidf_df.to_dict()
        return  words_tf_idf_dict, words_tfidf_df

    def poswords_tf_idf(self):
        poswords = self.df['poswords'].dropna()
        poswords_tf_dict = calculate_tf(poswords).to_dict()  
        poswords_tfidf_dict = calculate_tfidf(poswords).to_dict()  
        return  poswords_tf_dict, poswords_tfidf_dict
               
    def negwords_tf_idf(self):
        negwords = self.df['negwords'].dropna()
        negwords_tf_dict = calculate_tf(negwords).to_dict()  
        negswords_tfidf_dict  = calculate_tfidf(negwords).to_dict()  
        negswords_tfidf_df = calculate_tfidf(negwords)[0]
        return  negwords_tf_dict, negswords_tfidf_dict, negswords_tfidf_df

    def Media_category_data(self):
        S_total = self.df.groupby('Media_category').count()['content']
        df_total = S_total.reset_index().rename(columns = {'Media_category':'媒体类型', 'content':'总数据量'})
        df_total['占比'] = df_total['总数据量'].apply(lambda x: x/self.df.shape[0]).apply(lambda f: '%.2f' % (f*100)+'%')
        Media_distribution_df = df_total.rename(columns = {'总数据量':'数据量'})

        S_pos = self.df[self.df['Machine_emotion_lable']=='积极'].groupby('Media_category').count()['content']
        df_pos = S_pos.reset_index().rename(columns = {'Media_category':'媒体类型', 'content':'正面数据'})
        S_neg = self.df[self.df['Machine_emotion_lable']=='消极'].groupby('Media_category').count()['content']
        df_neg = S_neg.reset_index().rename(columns = {'Media_category':'媒体类型', 'content':'负面数据'})
        S_mid = self.df[self.df['Machine_emotion_lable']=='中性'].groupby('Media_category').count()['content']
        df_mid = S_mid.reset_index().rename(columns = {'Media_category':'媒体类型', 'content':'中性数据'})
        Media_count_df = pd.merge(df_total[['媒体类型','总数据量']], df_pos, how='outer', on='媒体类型')    
        Media_count_df = Media_count_df.merge(df_neg, how='outer', on='媒体类型')    
        Media_count_df =  Media_count_df.merge(df_mid, how='outer', on='媒体类型')
        Media_count_df.sort_values('总数据量', ascending=False, inplace=True)
        Media_count_df.reset_index(drop=True, inplace=True)
        Media_count_df['正面占比'] = (Media_count_df['正面数据']/Media_count_df['总数据量']).fillna(0).apply(lambda f: '%.2f' % (f*100)+'%')
        Media_count_df['负面占比'] = (Media_count_df['负面数据']/Media_count_df['总数据量']).fillna(0).apply(lambda f: '%.2f' % (f*100)+'%')
        Media_count_df['中性占比'] = (Media_count_df['中性数据']/Media_count_df['总数据量']).fillna(0).apply(lambda f: '%.2f' % (f*100)+'%')
        Media_count_df = Media_count_df[['媒体类型','正面数据','正面占比','负面数据','负面占比','中性数据','中性占比']].fillna(0)

        hot_Media_df = self.df.groupby(['Media_category','source']).count()['content'].reset_index()
        hot_Media_df.rename(columns={'Media_category':'媒体类型','source':'媒体名称', 'content':'文章数量'}, inplace=True)
        hot_Media_df = hot_Media_df.sort_values('文章数量', ascending = False)
        return Media_count_df, Media_distribution_df, hot_Media_df
    
    def Media_content(self):
        content = {}
        Media_tendency_df_max_time = self.Media_tendency_df.max()['监测时间']
        Media_tendency_df_max = self.Media_tendency_df.max()[self.Media_tendency_df.max()==self.Media_tendency_df.max().drop('监测时间').max()]
        content['声浪最高媒体']={}
        content['声浪最高媒体']['监测时间'] =  Media_tendency_df_max_time 
        content['声浪最高媒体']['媒体类型'] =  Media_tendency_df_max.index.tolist()[0]
        content['声浪最高媒体']['数量'] =  Media_tendency_df_max.values.tolist()[0]
        # print(content['声浪最高媒体'])
        content['声浪最高媒体'] = dict([(x,str(y)) for x,y in content['声浪最高媒体'].items()])
        content['信息最多媒体类型'] =  self.Media_category_data()[1].sort_values('数据量', ascending=False).head(1).max().to_dict()
        content['信息最多媒体类型'] = dict([(x,str(y)) for x,y in content['信息最多媒体类型'].items()])
        content['负面信息最多媒体类型'] = self.Media_category_data()[0].sort_values('负面数据', ascending=False)[['媒体类型','负面数据']].head(1).max().to_dict()
        content['负面信息最多媒体类型'] = dict([(x,str(y)) for x,y in content['负面信息最多媒体类型'].items()])
        content['最活跃媒体'] = self.Media_category_data()[2].sort_values('文章数量', ascending=False).head(1).max().to_dict()
        content['最活跃媒体'] = dict([(x,str(y)) for x,y in content['最活跃媒体'].items()])
        content_text={}

        content_text['媒体趋势'] = '{}声浪最高类媒体是{},共{}条信息'.format(content['声浪最高媒体']['监测时间'], content['声浪最高媒体']['媒体类型'], content['声浪最高媒体']['数量'])
        content_text['媒体分布'] = '在监测周期内{}类媒体声浪最高，共{}条信息，占比{}'.format(content['信息最多媒体类型']['媒体类型'],\
                       content['信息最多媒体类型']['数据量'], content['信息最多媒体类型']['占比'])
        # content_text['负面信息最多媒体类型'] = '在监测周期内{}负面信息最多，共{}条'.format(content['负面信息最多媒体类型']['媒体类型'], content['负面信息最多媒体类型']['负面数据'])
        content_text['负面信息最多媒体类型'] = ""
        content_text['最活跃媒体'] = '在监测周期内{}最活跃，共{}条信息'.format(content['最活跃媒体']['媒体名称'], content['最活跃媒体']['文章数量'])
        
        return content_text

    def weibo_tendency(self):
        time_quantum = pd.DataFrame({'监测时间':self.tendency_df['time_quantum'].unique()})
        tend_tendency_df = self.tendency_df[self.tendency_df['Media_category']=='微博'].pivot_table(index='time_quantum',columns='Machine_emotion_lable',values='Media_category',aggfunc='count')
        tend_tendency_df.index.rename('监测时间', inplace=True)
        tend_tendency_df.reset_index(inplace=True) 
        if '中性' not in tend_tendency_df.columns:
            tend_tendency_df['中性'] = np.nan
        if '积极' not in tend_tendency_df.columns:
            tend_tendency_df['积极'] = np.nan
        if '消极' not in tend_tendency_df.columns:
            tend_tendency_df['消极'] = np.nan      
        tend_tendency_df = pd.merge(time_quantum, tend_tendency_df, how='left', on='监测时间') 
        tend_tendency_df['监测时间'] = tend_tendency_df['监测时间'].astype(str)
        tend_tendency_df.fillna(0,inplace=True)  
        return tend_tendency_df     
        
    def weibo_rate(self):
        weibo_rate_df =  self.rate(self.weibo_df)
        weibo_rate_df['占比'] = weibo_rate_df['占比'].apply(lambda f: '%.2f' % (f*100)+'%')
        return weibo_rate_df
         
    def weibo_words_tf_idf(self):
        weibo_words = self.weibo_df['seg_words']
        tf_dict = calculate_tf(weibo_words)[1]
        tfidf_dict  = calculate_tfidf(weibo_words)[1]
        return tf_dict, tfidf_dict

    def Big_V_type_count(self):
        count1 = self.weibo_df['Big_V_type'][self.weibo_df['Big_V_type']=="名人"].count()
        count2 = self.weibo_df['Big_V_type'][self.weibo_df['Big_V_type']=="政府"].count()
        count3 = self.weibo_df['Big_V_type'][self.weibo_df['Big_V_type']=="企业"].count()
        count4 = self.weibo_df['Big_V_type'][self.weibo_df['Big_V_type']=="媒体"].count()    
        count5 = self.weibo_df['Big_V_type'][self.weibo_df['Big_V_type']=="其他"].count()                
        weibo_big_v_count_df = pd.DataFrame({"大V类型":["名人","政府","企业","媒体","其他"], "数据量":[count1,count2,count3,count4,count5]})
        weibo_big_v_count_df["占比"] = weibo_big_v_count_df["数据量"].apply(lambda x : x/self.weibo_df.shape[0]).fillna(0).apply(lambda f: '%.2f' % (f*100)+'%')
        return weibo_big_v_count_df

    def Amount_of_fans(self):
        self.weibo_df['Fans_level'] = self.weibo_df['Number_of_Fans'].apply(self.fans_level)
        fans_df = self.weibo_df.pivot_table(index='Fans_level',columns='Big_V_type',values='content',aggfunc='count')
        fans_df.index.rename('粉丝数量', inplace=True)
        fans_df.reset_index(inplace=True)
        Fans_level_df = pd.DataFrame({'粉丝数量':["粉丝数>1000w", "粉丝数>500w","粉丝数>100w","粉丝数>50w","粉丝数>20w","粉丝数>10w"],
                                      'rank':[0, 1, 2, 3, 4, 5]})
        fans_amount_df = fans_df.merge(Fans_level_df, how='right', on='粉丝数量')
        fans_amount_df.sort_values('rank', inplace=True)
        fans_amount_df.drop('rank', axis=1, inplace=True)
        for column in ["名人","政府","企业","媒体","其他"]:
            if column not in fans_amount_df.columns:
                fans_amount_df[column] = np.nan
        fans_amount_df_total = fans_amount_df.drop('粉丝数量', axis=1).apply(np.sum, axis=1)
        fans_amount_df.insert(1, '合计', fans_amount_df_total )
        fans_amount_df.fillna(0, inplace=True)
        return fans_amount_df

    def fans_level(self, count):
        Fans_level = ''
        if count >1000:
            Fans_level = "粉丝数>1000w"
        elif count >500:
            Fans_level = "粉丝数>500w"
        elif count >100:
            Fans_level = "粉丝数>100w"
        elif count >50:
            Fans_level = "粉丝数>50w"       
        elif count >20:
            Fans_level = "粉丝数>20w"   
        elif count >10:
            Fans_level = "粉丝数>10w"     
        return Fans_level        






