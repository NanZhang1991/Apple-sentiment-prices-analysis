
import pandas as pd

def pre_warning(df, parameter):
    rate_df = parameter.rate(df)
    pos_rate_df = rate_df['占比'][rate_df['类别'] == '负面']
    if (not pos_rate_df.empty) :
       pos_rate = pos_rate_df.tolist()[0]
    else:
       pos_rate = 0
    if pos_rate >0.6:
        color = '红色'
    else:
        color = '正常'

    authority_rate_df = parameter.rate(df[df['Media_category']=='政府或研究机构'])
    authoriyty_pos_rate_s = authority_rate_df['占比'][rate_df['类别'] == '负面']
    if (not authoriyty_pos_rate_s.empty) :
        authoriyty_pos_rate = authoriyty_pos_rate_s.tolist()[0]
    else:
        authoriyty_pos_rate = 0
    if authoriyty_pos_rate >0.2:
        authority_color = '橙色'
    else:
        authority_color ='正常'
    warning_df = pd.DataFrame({'类型':['总体','政府或研究机构'], '颜色':[ color, authority_color],'负面比':[pos_rate, authoriyty_pos_rate]})
    warning_df['负面比'] = warning_df['负面比'].apply(lambda f: '%.2f' % (f*100)+'%')
    weibo_df = df[(df['Media_category']=='微博') & (df['Machine_emotion_lable']=='消极')]
    if weibo_df.empty == False:
        weibo_forward = weibo_df['Amount_of_forward'].sum()
        if weibo_forward >10000:
            weibo_forward_color ="黄色"
        else:
            weibo_forward_color ='正常'

        weibo_forward_person_s = weibo_df['Amount_of_forward'][weibo_df['Big_V_type']=='名人']
        weibo_forward_person =  weibo_forward_person_s.sum()
        if weibo_forward_person >5000:
            weibo_forward_person_color ="黄色"
        else:
            weibo_forward_person_color ='正常'

        weibo_forward_government_s = weibo_df['Amount_of_forward'][weibo_df['Big_V_type']=='政府']
        weibo_forward_government = weibo_forward_government_s.sum()
        if weibo_forward_government >100:
            weibo_forward_government_color ="黄色"
        else:
            weibo_forward_government_color ='正常'

        weibo_forward_media_s = weibo_df['Amount_of_forward'][weibo_df['Big_V_type']=='媒体']
        weibo_forward_media = weibo_forward_media_s.sum()
        print('123', weibo_forward_media_s)
        if weibo_forward_media >1000:
            weibo_forward_media_color ="黄色"
        else:
            weibo_forward_media_color ='正常'

        weibo_forward_company_s = weibo_df['Amount_of_forward'][weibo_df['Big_V_type']=='企业']
        weibo_forward_company = weibo_forward_company_s.sum()
        if weibo_forward_company >1000:
            weibo_forward_company_color ="黄色"
        else:
            weibo_forward_company_color ='正常'

        
        
        weibo_warning_df = pd.DataFrame({'类型':['微博总体','微博名人','微博政府','微博媒体','微博企业'],
                                '颜色':[weibo_forward_color, weibo_forward_person_color, weibo_forward_government_color, weibo_forward_media_color, weibo_forward_company_color],
                                '负面转发数':[weibo_forward, weibo_forward_person, weibo_forward_government, weibo_forward_media, weibo_forward_company]})   
    else:
        weibo_warning_df = pd.DataFrame()   
    return warning_df, weibo_warning_df


    









    



