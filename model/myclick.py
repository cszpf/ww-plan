# encoding=utf-8
import requests as rq
import json
import pandas as pd
import datetime
import os
import re
from tqdm import tqdm
from Cookie import Cookie

# 获取当前日期
TODAY = datetime.date.today()
# 需定期更新cookie，否则无法爬取页面数据，设置session动态会话
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    
html = '''https://web.umeng.com/main.php?c=cont&a=page&ajax=module=summarysource|module=safeinfo|module=statistics_orderBy=pv_orderType=-1_dataType=source_currentPage={page}_pageType=30&st={date}&et={date}'''


# columns = ['受访页面', '浏览次数(PV)', '独立访客(UV)', 'IP', '人均浏览页数', '页面停留时间', '输出PV', '平均页面停留时间']
# 获取映射规则
def getRule(path='../static/rules.txt'):
    if not os.path.exists(path):
        path = './static/rules.txt'
    rules = pd.read_csv(path, sep='\s+', header=None)
    rules.columns = ['id', 'name']
    return rules

# 映射
def mapping(data, rule):
    # data<pd.DataFrame>, rule<pd.DataFrame>
    def mapRule(x, rule):
        for i in rule.index:
            if rule['id'].loc[i] in x:
                return rule['name'].loc[i]
        return 'xxx'
    data['受访页面'] = data['受访页面'].apply(lambda x: mapRule(x, rule))
    data = data[data['受访页面'] != 'xxx']
    return data.groupby(['受访页面'], as_index=False, sort=False).agg('sum')
        
# 获得指定指定日期的点击量记录
def getDateClick(date, rule=getRule()):
    # date.format like 'YYYY-mm-dd'
    columns = ['受访页面', '{}'.format(date)]
    clicks = []
    for page in range(1, 300):
        _html = html.format(page=page, date=date)
        # print(_html)
        result = rq.get(_html, headers=headers)
        data = json.loads(result.text)
        data = data['data']
        if 'statistics' in data.keys() and data['statistics'] != '':
            for _ in data['statistics']['items']:
                # type(_) is dict
                # clicks.append(list(_.values()))
                clicks.append([_['source'], _['pv']])
        else:
            break
    df = pd.DataFrame(clicks,columns=columns)
    df[columns[1]] = df[columns[1]].apply(int)
    return mapping(df, rule)

# 获得一段日期的点击量
def preDate(startDate1='2018-06-15', endDate1=TODAY):
    cookie = Cookie()
    headers.update({'Cookie':';'.join(['%s=%s'%(i,j) for i,j in cookie.get_cookie_from_network().items()])})
    def splitDate(string):
        return [int(_) for _ in string.split('-')]
    startDate = splitDate(startDate1)
    startdate = datetime.date(startDate[0], startDate[1], startDate[2])
    today = endDate1 if type(endDate1) is datetime.date else datetime.date(splitDate(endDate1)[0],splitDate(endDate1)[1],splitDate(endDate1)[2])
    print('Starting to crawl data....')
    results = None; rules = getRule()
    for i in tqdm(range((today - startdate).days)):
        date = startdate + datetime.timedelta(i)
        result = getDateClick(date.strftime('%Y-%m-%d'), rules)
        # break
        if i == 0:
            results = result
        else:
            results = results.merge(result, how='outer', on='受访页面', copy=False)
    print('Crawling data from {} to {} has finished!'.format(startDate1, date.strftime('%Y-%m-%d')))
    return all_click(results.fillna(0))

# 汇总每个页面的所有点击数
def all_click(df, rules=['首页','支付页','本店券','邻店券']):
    df1 = df.copy()
    for _ in rules:
        ss = pd.DataFrame(df[[_ in i for i in df['受访页面']]].sum()).T
        ss['受访页面'] = ['{}（所有点击）'.format(_)]
        df1 = pd.concat([df1,ss], ignore_index=True)
    del(ss)
    df1.sort_values(by='受访页面', inplace=True)
    return df1

def write_csv(df, path='../static/click'):
    if not os.path.exists(path):
        os.makedirs(path)
    df.to_csv(os.path.join(path,'click.csv'), index=False, encoding='GBK')
    print('saving data has finished!')

if __name__ == '__main__':
    # mapping()
    # cookie = Cookie()
    # headers.update({'Cookie':';'.join(['%s=%s'%(i,j) for i,j in cookie.get_cookie_from_network().items()])})
    # df = getDateClick('2018-08-01')
    df = preDate()
    write_csv(df)