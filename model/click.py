# encoding=utf-8
import requests as rq
import json
import pandas as pd
import datetime
import os
import re
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Cookie': 'PHPSESSID=v5f19l6ud48735hgvh0hcc3cp2; UM_distinctid=164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e; CNZZDATA33222=cnzz_eid%3D1855708765-1532915522-http%253A%252F%252Fweb.umeng.com%252F%26ntime%3D1532915522; uc_session_id=30ce56c0-727b-430b-86b0-94ce1d3497ec; cna=jdjME+BMrU8CAd7JiwTBmHlO; umplus_uc_token=19GdJNGxHUpRGpHoJI-Hk3w_5a6dfac7aec84a2d831926bd7ff881aa; umplus_uc_loginid=412606846%40qq.com; from=umeng; edtoken=cnzz_5b5e7a94cb553; frontvar=siteShowHis%3Dopen%26cmenu%3D0%26lns%3Dmenu-1%2Cflow-1%2Ctraf-1%2Ccont-1%2Cvisitor-1%2Cbigdata-1%2Cindustry-1%2Ceanalysis-1%2C; CNZZDATA30086426=cnzz_eid%3D1997450440-1532917914-http%253A%252F%252Fweb.umeng.com%252F%26ntime%3D1532916505; cn_1258498910_dplus=1%5B%7B%7D%2C0%2C1532919707%2C0%2C1532919707%2Cnull%2C%22164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e%22%2C%221532913569%22%2C%22http%3A%2F%2Fweb.umeng.com%2Fmain.php%3Fc%3Duser%26a%3Dtip%26code%3D1000%26param3%3DaHR0cHM6Ly93ZWIudW1lbmcuY29tL21haW4ucGhwP2M9Y29udCZhPWZyYW1lJnNpdGVpZD0xMjczOTYzMjk4%26channel%3D%2523%2521%2F1529030080126%2Fcont%2Fpage%2F1%2F1273963298%2F2018-06-15%2F2018-06-15%22%2C%22web.umeng.com%22%5D; isg=BPj4FyQG1wURLjuBmCY4ehvIyaZKyV3UmWtaizJpRDPmTZg32nEsew4sAQXYHRTD; cn_ea1523f470091651998a_dplus=%7B%22distinct_id%22%3A%20%22164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201532919711%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201532919711%7D%2C%22initial_view_time%22%3A%20%221532918422%22%2C%22initial_referrer%22%3A%20%22https%3A%2F%2Fpassport.umeng.com%2Flogin%3FappId%3Dcnzz%22%2C%22initial_referrer_domain%22%3A%20%22passport.umeng.com%22%7D; _cnzz_CV30069868=%E6%98%AF%E5%90%A6%E7%99%BB%E5%BD%95%7C%E6%AD%A3%E5%B8%B8%E7%99%BB%E5%BD%95%7C1532948487881; CNZZDATA30069868=cnzz_eid%3D1903705378-1532913177-http%253A%252F%252Fweb.umeng.com%252F%26ntime%3D1532915178; CNZZDATA30001831=cnzz_eid%3D1249785746-1532917063-http%253A%252F%252Fweb.umeng.com%252F%26ntime%3D1532914963'
    }
    
html = '''https://web.umeng.com/main.php?c=cont&a=page&ajax=module=summarysource|module=safeinfo|module=statistics_orderBy=pv_orderType=-1_dataType=source_currentPage={page}_pageType=30&st={date}&et={date}'''


# columns = ['受访页面', '浏览次数(PV)', '独立访客(UV)', 'IP', '人均浏览页数', '页面停留时间', '输出PV', '平均页面停留时间']
# 获取映射规则
def getRule():
    rules = pd.read_csv('../static/rules.txt', sep='\s+', header=None)
    rules.columns = ['id', 'name']
    return rules

# 映射
def mapping(data, rule):
    # data<pd.DataFrame>, rule<pd.DataFrame>
    def mapRule(x, rule):
        for i in rule.index:
            if rule['id'].loc[i] in x:
                return rule['name'].loc[i]
        return x
    data = data.applymap(lambda x: mapRule(x, rule))
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
                clicks.append(list(_.values())[:2])
        else:
            break
    df = pd.DataFrame(clicks,columns=columns)
    return mapping(df, rule)

# 获得当前天数之前的点击量
def preDate(startDate1='2018-06-15'):
    def splitDate(string):
        return [int(_) for _ in string.split('-')]
    startDate = splitDate(startDate1)
    startdate = datetime.date(startDate[0], startDate[1], startDate[2])
    today = datetime.date.today()
    print('Starting to crawl data....')
    results = None
    for i in tqdm(range((today - startdate).days)):
        date = startdate + datetime.timedelta(i)
        result = getDateClick(date.strftime('%Y-%m-%d'))
        # break
        if i == 0:
            results = result
        else:
            results = results.merge(result, how='outer', on='受访页面', copy=False)
    if not os.path.exists('../static/click'):
        os.makedirs('../static/click')
    results.fillna(0).to_csv('../static/click/click.csv', index=False)
    print('Crawling data from {} to {} has finished!'.format(startDate1, date.strftime('%Y-%m-%d')))
    return results.fillna(0)
    
if __name__ == '__main__':
    preDate()
    # mapping()
