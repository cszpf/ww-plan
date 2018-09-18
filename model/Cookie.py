# coding='UTF-8'
import os
import time
import requests
false = False
true = True
_cookie = 'cn_1259864772_dplus=1%5B%7B%22%E6%98%AF%E5%90%A6%E7%99%BB%E5%BD%95%22%3Atrue%2C%22UserID%22%3A%22412606846%40qq.com%22%7D%2C0%2C1533656307%2C0%2C1533656307%2Cnull%2C%22164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e%22%2C%221533654484%22%2C%22https%3A%2F%2Fmobile.umeng.com%2Fapps%22%2C%22mobile.umeng.com%22%5D; cna=LzXwE7Fb3SkCAd7JiwQV0nGW; PHPSESSID=ruv9big130r0uii5tr3otfbub4; UM_distinctid=164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e; um_lang=zh; edtoken=cnzz_5b86cfc39a653; from=umeng; frontvar=siteShowHis%3Dopen%26siteListSortId%3D4%26cmenu%3D0; uc_session_id=8984c9e4-8d5f-417c-a6b7-bce76dc12cf9; umplus_uc_token=1pskq7LeDT7Q1j5gwLPB_RQ_aa52bc9fb7084ab1b2e38efe26adc978; umplus_uc_loginid=412606846%40qq.com; CNZZDATA1258498910=4900034-1533654459-https%253A%252F%252Faccount.umeng.com%252F%7C1535605910; cn_1258498910_dplus=1%5B%7B%22userid%22%3A%22412606846%40qq.com%22%7D%2C0%2C1535607057%2C0%2C1535607057%2C%22%24direct%22%2C%22164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e%22%2C%221532913569%22%2C%22http%3A%2F%2Fweb.umeng.com%2Fmain.php%3Fc%3Duser%26a%3Dtip%26code%3D1000%26param3%3DaHR0cHM6Ly93ZWIudW1lbmcuY29tL21haW4ucGhwP2M9Y29udCZhPWZyYW1lJnNpdGVpZD0xMjczOTYzMjk4%26channel%3D%2523%2521%2F1529030080126%2Fcont%2Fpage%2F1%2F1273963298%2F2018-06-15%2F2018-06-15%22%2C%22web.umeng.com%22%5D; isg=BM_PEeVDyEEsaszSJBMvZ3PJXmMZXCGTmuZN7uHcHz5DsO6y6cbbZ06htqCryPuO; CNZZDATA30086426=cnzz_eid%3D1281187739-1533626752-%26ntime%3D1535604672; CNZZDATA33222=cnzz_eid%3D1207451176-1533625464-%26ntime%3D1535604143; _cnzz_CV30069868=%E6%98%AF%E5%90%A6%E7%99%BB%E5%BD%95%7C%E6%AD%A3%E5%B8%B8%E7%99%BB%E5%BD%95%7C1535635859272; CNZZDATA30069868=cnzz_eid%3D987871338-1533625979-%26ntime%3D1535603944; CNZZDATA30001831=cnzz_eid%3D75532440-1533624470-%26ntime%3D1535605220; cn_ea1523f470091651998a_dplus=%7B%22distinct_id%22%3A%20%22164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201535607092%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201535607092%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D%2C%22initial_view_time%22%3A%20%221533621991%22%2C%22initial_referrer%22%3A%20%22https%3A%2F%2Faccount.umeng.com%2F%22%2C%22initial_referrer_domain%22%3A%20%22account.umeng.com%22%7D'
_cookie = [
{
    "domain": ".umeng.com",
    "expirationDate": 1568765998,
    "hostOnly": false,
    "httpOnly": false,
    "name": "cn_1258498910_dplus",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1%5B%7B%22userid%22%3A%22412606846%40qq.com%22%7D%2C0%2C1537229997%2C0%2C1537229997%2C%22cn.bing.com%22%2C%22164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e%22%2C%221532913569%22%2C%22http%3A%2F%2Fweb.umeng.com%2Fmain.php%3Fc%3Duser%26a%3Dtip%26code%3D1000%26param3%3DaHR0cHM6Ly93ZWIudW1lbmcuY29tL21haW4ucGhwP2M9Y29udCZhPWZyYW1lJnNpdGVpZD0xMjczOTYzMjk4%26channel%3D%2523%2521%2F1529030080126%2Fcont%2Fpage%2F1%2F1273963298%2F2018-06-15%2F2018-06-15%22%2C%22web.umeng.com%22%5D",
    "id": 1
},
{
    "domain": ".umeng.com",
    "expirationDate": 1565192307,
    "hostOnly": false,
    "httpOnly": false,
    "name": "cn_1259864772_dplus",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1%5B%7B%22%E6%98%AF%E5%90%A6%E7%99%BB%E5%BD%95%22%3Atrue%2C%22UserID%22%3A%22412606846%40qq.com%22%7D%2C0%2C1533656307%2C0%2C1533656307%2Cnull%2C%22164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e%22%2C%221533654484%22%2C%22https%3A%2F%2Fmobile.umeng.com%2Fapps%22%2C%22mobile.umeng.com%22%5D",
    "id": 2
},
{
    "domain": ".umeng.com",
    "expirationDate": 1568720109,
    "hostOnly": false,
    "httpOnly": false,
    "name": "cn_ea1523f470091651998a_dplus",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "%7B%22distinct_id%22%3A%20%22164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201537184109%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201537184109%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D%2C%22initial_view_time%22%3A%20%221533621991%22%2C%22initial_referrer%22%3A%20%22https%3A%2F%2Faccount.umeng.com%2F%22%2C%22initial_referrer_domain%22%3A%20%22account.umeng.com%22%7D",
    "id": 3
},
{
    "domain": ".umeng.com",
    "expirationDate": 2164346158,
    "hostOnly": false,
    "httpOnly": false,
    "name": "cna",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "LzXwE7Fb3SkCAd7JiwQV0nGW",
    "id": 4
},
{
    "domain": ".umeng.com",
    "expirationDate": 1552781999,
    "hostOnly": false,
    "httpOnly": false,
    "name": "isg",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "BISEdx1Og9deHjfTuwq0toSQVQK2NakVi2LCVJ4lEM8SySSTxq14l7prDSG0UeBf",
    "id": 5
},
{
    "domain": ".umeng.com",
    "hostOnly": false,
    "httpOnly": true,
    "name": "PHPSESSID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "hbdbsi61n43gufgf8c0qkc32v0",
    "id": 6
},
{
    "domain": ".umeng.com",
    "expirationDate": 1569323017,
    "hostOnly": false,
    "httpOnly": false,
    "name": "uc_session_id",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "32575356-f692-435d-aa13-985c65b4195d",
    "id": 7
},
{
    "domain": ".umeng.com",
    "expirationDate": 1568765998,
    "hostOnly": false,
    "httpOnly": false,
    "name": "UM_distinctid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e",
    "id": 8
},
{
    "domain": ".umeng.com",
    "expirationDate": 1565192301,
    "hostOnly": false,
    "httpOnly": false,
    "name": "um_lang",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "zh",
    "id": 9
},
{
    "domain": ".umeng.com",
    "expirationDate": 1569370797,
    "hostOnly": false,
    "httpOnly": false,
    "name": "umplus_uc_loginid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "412606846%40qq.com",
    "id": 10
},
{
    "domain": ".umeng.com",
    "expirationDate": 1569370797,
    "hostOnly": false,
    "httpOnly": false,
    "name": "umplus_uc_token",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1ktdF-ShBBzZBUT7D-gSdaQ_780baafeb6cd43ef9c5593536af530b3",
    "id": 11
},
{
    "domain": "www.umeng.com",
    "expirationDate": 1552954798,
    "hostOnly": true,
    "httpOnly": false,
    "name": "CNZZDATA1258498910",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1619167061-1533654459-https%253A%252F%252Fcn.bing.com%252F%7C1537225847",
    "id": 12
}
]

def cookieFormat(cookies):
    # return {i.split('=')[0]:i.split('=')[1] for i in cookies.strip().split('; ')}
    return {i['name']:i['value'] for i in cookies}

class Cookie:
    def __init__(self):
        self.password2 = '57a8e67e39df4eb091899f5f8ab0b6284641e1f3b9fbb58bbaf199477f3070f8b333a223e65e7a581e3f03e38a117ff756b6325fa087878e3b72c79af393b2267400a413e27b79dacc55d7804b3be8b9c3ddf90323c422b2528bc8bb042c31a4303dca0c5f7643ba6ff6422161d7670a0fa09a10552fdc5ea4c585e531662f24'
        self.loginId = '412606846@qq.com'
        self.password = 'weileFUMU1314'
        self.login_url = 'https://passport.alibaba.com/newlogin/login.do?fromSite=-2&appName=youmeng'
        self.heads = {
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
        }

    # 用selenium部分更新cookies的方式
    def get_cookie_from_network(self):
        COOKIE = cookieFormat(_cookie)
        # x = requests.get('https://web.umeng.com/main.php?c=cont&a=page&ajax=module=summarysource|module=safeinfo|module=statistics_orderBy=pv_orderType=-1_dataType=source_currentPage=1_pageType=30&st=20180617&et=20180820',cookies=COOKIE)
        # print(x.text)
        return COOKIE

if __name__ == '__main__':
    cookie = Cookie()
    cookie.get_cookie_from_network()