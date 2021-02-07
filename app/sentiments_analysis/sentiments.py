# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 11:21:03 2020

@author: YJ001
"""
import numpy as np
import pandas as pd
import os
from app.text_process.text_process import language_category,  en_del_stopwords, cn_tokenize, cn_del_stopwords, cn_cut_sentence, seg_words
from nltk import tokenize  
from nltk.tokenize import word_tokenize

# 获取中文六种权值的词，根据要求返回list，
cn_weighted_value = pd.read_excel('app/NLP_source/情感极性词典.xlsx')
#print("reading chinese sentiment dict ...")
#读取中文情感词典
cn_posdict = cn_weighted_value['cn_posdict'].dropna()
cn_negdict = cn_weighted_value['cn_negdict'].dropna()
# 读取程度副词词典
# 权值为2
cn_mostdict = cn_weighted_value['cn_mostdict'].dropna()
# 权值为1.75
cn_verydict = cn_weighted_value['cn_verydict'].dropna()
# 权值为1.50
cn_moredict = cn_weighted_value['cn_moredict'].dropna()
# 权值为1.25
cn_ishdict = cn_weighted_value['cn_ishdict'].dropna()
# 权值为0.25
cn_insufficientdict = cn_weighted_value['cn_insufficientdict'].dropna()
# 权值为-1
cn_inversedict = cn_weighted_value['cn_inversedict'].dropna()

#程度副词处理，对不同的程度副词给予不同的权重
def cn_match_adverb(word,sentiment_value):
    #最高级权重为
    if word in cn_mostdict.values:
        sentiment_value *= 8
    #比较级权重
    elif word in cn_verydict.values:
        sentiment_value *= 6
    #比较级权重
    elif word in cn_moredict.values:
        sentiment_value *= 4
    #轻微程度词权重
    elif word in cn_ishdict.values:
        sentiment_value *= 2
    #相对程度词权重
    elif word in cn_insufficientdict.values:
        sentiment_value *= 0.5
    #否定词权重
    elif word in cn_inversedict.values:
        sentiment_value *= -1
    else:
        sentiment_value *= 1
    return sentiment_value


#对中文每一句文字打分 
def cn_tag_word(seg_words):
    #i，s 记录情感词和程度词出现的位置
    i = 0   #记录扫描到的词位子
    s = 0   #记录情感词的位置
    poscount = 0 #记录积极情感词数目
    negcount = 0 #记录消极情感词数目  
    #逐个查找情感词      
    for word in seg_words:
        #如果为积极词
        if word in cn_posdict.values:
            poscount += 1  #情感词数目加1
        #在情感词前面寻找程度副词
            for w in seg_words[s:i]:
                poscount = cn_match_adverb(w,poscount)
            s = i+1 #记录情感词位置
        # 如果是消极情感词
        elif word in cn_negdict.values:
            negcount +=1
            for w in seg_words[s:i]:
                negcount = cn_match_adverb(w,negcount)
            s = i+1
        #如果结尾为感叹号或者问号，表示句子结束，并且倒序查找感叹号前的情感词，权重+4
        elif word =='!' or  word =='！' or word =='?' or word == '？':
            for w2 in seg_words[::-1]:
                #如果为积极词，poscount+2
                if w2 in cn_posdict.values:
                    poscount += 4
                    break
                #如果是消极词，negcount+2
                elif w2 in cn_negdict.values:
                    negcount += 4
                    break
        i += 1 #定位情感词的位置
     #计算情感值
    sentiment_score = poscount - negcount
    return sentiment_score
 
def cn_find_emo_word(seg_words):
    poswords = []
    negwords = []                  
    for word in seg_words:
        if word in cn_posdict.values:            
            poswords.append(word)
        elif word in cn_negdict.values:
            negwords.append(word)
    return poswords, negwords


    
#中文文章打分   
def cn_single_sentiment_score(text_sent):   
    sentiment_sum = 0
    #对文章进行分句
    sentence_list = cn_cut_sentence(text_sent)
    for sent in sentence_list:
        words = cn_tokenize(sent)
        seg_words =cn_del_stopwords(words)
        sentiment_score = cn_tag_word(seg_words)       
        sentiment_sum += sentiment_score
    return sentiment_sum

#读取英文情感词典
en_weighted_value = pd.read_excel(r'app/NLP_source/sentiment.xlsx')
#print("reading english sentiment dict ...")
en_posdict = pd.concat([en_weighted_value['postive_comment'].str.strip(),en_weighted_value['postive_emotions'].str.strip()])
en_negdict = pd.concat([en_weighted_value['negtive_comment'].str.strip(),en_weighted_value['negtive_emotions'].str.strip()])
# 获取取程度副词词典
# 权值为2
en_mostdict = en_weighted_value['most'].str.strip().dropna()
# 权值为1.75
en_verydict = en_weighted_value['very'].str.strip().dropna()
# 权值为1.50
en_moredict = en_weighted_value['more'].str.strip().dropna()
# 权值为1.25
en_ishdict = en_weighted_value['ish'].str.strip().dropna()
# 权值为0.25
en_insufficientdict = en_weighted_value['insufficiently'].str.strip().dropna()
# 权值为-1
en_inversedict = en_weighted_value['inverse'].str.strip().dropna()

#英文程度副词处理，对不同的程度副词给予不同的权重
def en_match_adverb(word,sentiment_value):
    #最高级权重为
    if word in en_mostdict.values:
        sentiment_value *= 8
    #比较级权重
    elif word in en_verydict.values:
        sentiment_value *= 6
    #比较级权重
    elif word in en_moredict.values:
        sentiment_value *= 4
    #轻微程度词权重
    elif word in en_ishdict.values:
        sentiment_value *= 2
    #相对程度词权重
    elif word in en_insufficientdict.values:
        sentiment_value *= 0.5
    #否定词权重
    elif word in en_inversedict.values:
        sentiment_value *= -1
    else:
        sentiment_value *= 1
    return sentiment_value
 
def en_tag_word(seg_words):
    #i，s 记录情感词和程度词出现的位置
    i = 0   #记录扫描到的词位子
    s = 0   #记录情感词的位置
    poscount = 0 #记录积极情感词数目
    negcount = 0 #记录消极情感词数目  
    #逐个查找情感词      
    for word in seg_words:
        #如果为积极词
        if word in en_posdict.values:
            poscount += 1  #情感词数目加1
        #在情感词前面寻找程度副词
            for w in seg_words[s:i]:
                poscount = en_match_adverb(w,poscount)
            s = i+1 #记录情感词位置
        # 如果是消极情感词
        elif word in en_negdict.values:
            negcount +=1
            for w in seg_words[s:i]:
                negcount = en_match_adverb(w,negcount)
            s = i+1
        #如果结尾为感叹号或者问号，表示句子结束，并且倒序查找感叹号前的情感词，权重+4
        elif word =='!' or  word =='！' or word =='?' or word == '？':
            for w2 in seg_words[::-1]:
                #如果为积极词，poscount+2
                if w2 in en_posdict.values:
                    poscount += 4
                    break
                #如果是消极词，negcount+2
                elif w2 in en_negdict.values:
                    negcount += 4
                    break
        i += 1 #定位情感词的位置
     #计算情感值
    sentiment_score = poscount - negcount
    return sentiment_score

#英文文章打分
def en_single_sentiment_score(text_sent):   
    sentiment_sum = 0
    #对文章进行分句
    sentence_list = tokenize.sent_tokenize(text_sent)
    for sent in sentence_list:
        words = word_tokenize(sent)
        seg_words =en_del_stopwords(words)
        sentiment_score = en_tag_word(seg_words)       
        sentiment_sum += sentiment_score
    return sentiment_sum
 
def en_find_emo_word(seg_words):
    poswords = []
    negwords = []              
    for word in seg_words:
        if word in en_posdict.values:            
            poswords.append(word)
        elif word in en_negdict.values:
            negwords.append(word)
    return poswords, negwords

        
# 分析test_data.txt 中的所有文章，返回一个列表，列表中元素为（分值，文章）元组
def label(score):
    if pd.isnull(score) ==False:
        if score < 0:
            s = '消极'
        elif score == 0:
            s = '中性'
        else:
            s = '积极'
        return s
    else:
        return None


def run_score(df):
    df['score'] = np.nan
    df['score'][df['language']=="Chinese"] = df['content'][df['language']=="Chinese"].apply(cn_single_sentiment_score)
    df['score'][df['language']=="English"] = df['content'][df['language']=="English"].apply(en_single_sentiment_score)
    df['Machine_emotion_lable'] = df['score'].apply(label)                        
    return df


def emotion_words(df):
    df['seg_words_list'] = df['seg_words'].str.split(' ')
    df['emotion_words'] = ''
    # print("find Chinese emotion words...")
    df['emotion_words'][df['language']=="Chinese"] = df['seg_words_list'][df['language']=="Chinese"].apply(cn_find_emo_word)
    # print("find English emotion words ...")
    df['emotion_words'][df['language']=="English"] = df['seg_words_list'][df['language']=="English"].apply(en_find_emo_word)    
    df['poswords'] = df['emotion_words'].apply(lambda x: " ".join(x[0]))
    df['negwords'] = df['emotion_words'].apply(lambda x: " ".join(x[1]))
    return df    


def Media_category(text_sent):
    if ("网" in text_sent) or ("news" in text_sent) or ("新闻" in text_sent) :
        category = "新闻网站"
    elif ("会" in text_sent) or ("研究" in text_sent) or ("局" in text_sent) or ("政府" in text_sent):
        category = "政府或研究机构"
    elif "微博" in text_sent:
        category = "微博"
    elif "微信" in text_sent:
        category = "微信"
    elif ("论坛"in text_sent) or "评论"in text_sent:
        category = "评论"    
    elif "app" in text_sent:
        category = "app"       
    else:
        category = "其他"
    return category  
    

    
#主程序
if __name__ == '__main__':
    print('Processing...')
    #测试
#    sentence1 = '要怎么说呢! 我需要的恋爱不是现在的样子, 希望是能互相鼓励的勉励, 你现在的样子让我觉得很困惑。 你到底能不能陪我一直走下去, 你是否有决心?是否你看不惯我?你是可以随意的生活,但是我的未来我耽误不起！'
#    sentence2 = '转有用吗？这个事本来就是要全社会共同努力的，公交公司有没有培训到位？公交车上地铁站内有没有放足够的宣传标语？我现在转一下文章，没有多大的意义。'
#    sentences = [sentence1, sentence2]
#    sents_df = pd.DataFrame({'content': sentences})
#    scores = run_score(sents_df)
    

    comment_df = pd.read_csv(os.path.join(os.getcwd(), r'test\sentiment_test\sentiment_data_source\input\tea_hotspot.csv'))
        
    # df = comment_df.loc[0:1,['content']]
    df = comment_df.loc[209:211,['content']]
    df['language'] = df['content'].apply(language_category)  
    df_11 = seg_words(df)
    scores11 = run_score(df_11)     
    df_111 = emotion_words(df_11)

#    scores22 = run_score(comment_df2.loc[0:99,['content']])
#    print(scores22)

    print('finish...')