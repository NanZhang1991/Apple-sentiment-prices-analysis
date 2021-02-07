
依赖环境
在Yantai_apple_analysis路径下
windows终端 输入pip install -r requirements.txt
linux终端 输入 pip3 install -r requirements.txt

启动服务
在Yantai_apple_analysis路径下
windows终端 输入python run.py 启动服务
linux终端 输入python3 run.py 启动服务

后台挂起进程
nohup python3 run.py >/dev/null  2>&1 &

nohup python3 text_pre_pro.py >/dev/null 2>&1 &

nohup python3 report_cache.py >/dev/null 2>&1 &

数据库 
mysql_host = "198.18.69.1"
mysql_port = “30052”

价格指数原表:
零售和产地: bd_fruit_price 关联  bd_fruit_price_detail b
市场: abd_market_price

综合价格指数
http://apple.yantai.gov.cn/api/price_index/get_pri_i/<kind>
kind = from(产地), retail(零售), market(市场)
例如：http://apple.yantai.gov.cn/api/price_index/get_pri_i/market
输入：
start = "2020-7-1"
end = "2020-7-30"
返回结果:
{
{
  "date": {
    "0": "2020-02-28",
    "1": "2020-02-29",
    "2": "2020-03-01",
    "3": "2020-03-02",
    "4": "2020-03-03",
    "5": "2020-03-04",
  },
  "pi": {
    "0": "0.00",
    "1": "0.00",
    "2": "0.00",
    "3": "0.00",
    "4": "0.00",
    "5": "0.00",

  }
}
}
品种列表
http://apple.yantai.gov.cn/api/price_index/varietys/<kind>
kind = from(产地), retail(零售), market(市场)
例如：http://apple.yantai.gov.cn/api/price_index/varietys/from

输入：
start = "2020-7-1"
end = "2020-7-30"

返回结果:
[
  "澳洲青苹",
  "元帅",
  "红富士",
  "藤牧1号",
  "北斗"
]

不同品种价格指数
http://apple.yantai.gov.cn/api/price_index/svpi/<kind>
kind = from(产地), retail(零售), market(市场)
例如：http://apple.yantai.gov.cn/api/price_index/svpi/market
输入：
start = "2020-7-1"
end = "2020-7-30"
variety = 红富士
返回结果：
{
  "date": {
    "0": "2020-07-14",
    "1": "2020-07-16",
    "2": "2020-07-17",
    "3": "2020-07-20",
    "4": "2020-07-21",
    "5": "2020-07-22"
  },
  "svpi": {
    "0": "0.00",
    "1": "200.00",
    "2": "0.00",
    "3": "-56.00",
    "4": "-17.42",
    "5": "12.39"
  }
}





*分析报告 
http://apple.yantai.gov.cn/api/sentiments/report
数据: uid	title(文章标题)	 content(文本内容)	 detailurl(网址) source(来源) pubtime(发布时间), createtime(创建时间)
     Amount_of_forward(转发量) Number_of_Fans(粉丝量) Big_V_type(大V类型)	

舆情数据表:
原表: search_apple_news
预处理后的表: 2020_seg_sentiment_content

输入：start(起始时间) end(结束时间)
输出：

苹果舆情分析
监测周期：2020-05-20 00:00:00~2020-05-20 23:59:59


一、趋势分析
* "在整体发展趋势中，2020.05.20 00:00声量最高，共产生648条信息。在2020.05.20 00:00重要媒体声量最高，共产生38条信息。"
整体趋势
监测时间  全部声浪 重要媒体声浪 
# 某段时间内每个时间段监测的信息量

二、内容分析
（一）倾向性趋势
* "2020-01-01负面信息最多，共0.0条",
类型     时间   数据量
正面:
负面：
中性：
# 某段时间内每个时间段监测的正负面信息量

（二）倾向性分布
* "在监测周期内，共监测到20条信息，其中负面信息0条，占比0.00%。"
类型     数据量   占比
正面:
负面：
中性：
# 某段时间内整体的正负面数据量占比。

（三）热词分析
* "在监测周期内媒体和网民主要关注与年货、苹果、消费、记者、水果相关的信息"
1.热词词云
# 某段时间段内高频重点词汇


三、媒体分析
* "2020-01-16声浪最高类媒体是新闻网站,共4条信息",
（一）媒体趋势
监测时间 新闻网站 政府或研究机构 微博  微信 论坛 app 其他
# 某段时间段不同类别媒体信息数量

（二）媒体对比
* "在监测周期内新闻网站负面信息最多，共0.0条"
媒体类型 总数据量 正面数据 占比 负面数据量 占比 中性数据量 占比
# 某段时间段不同类别媒体正负面信息量统计和占比

（三）媒体分布
* "在监测周期内新闻网站类媒体声浪最高，共20条信息，占比100.00%",
媒体类型    数量   占比
新闻网站
政府或研究机构 
微博 
微信 
其他
# 某段时间不同类别媒体数量占比

（四）活跃媒体
* "在监测周期内cctv新闻最活跃，共5条信息",
全部媒体
媒体类型   媒体名称  文章数量 
新闻网站
政府或研究机构
微博  
微信
论坛
app
其他
# 不同类别媒体中活跃媒体文章数量


