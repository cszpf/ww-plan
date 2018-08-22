# encoding='UTF-8'
import pickle
import os
import time
import requests
import selenium
from selenium import webdriver

s = requests.Session()
COOKIES = "UM_distinctid=164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e; cna=LzXwE7Fb3SkCAd7JiwQV0nGW; um_lang=zh; cn_1259864772_dplus=1%5B%7B%22%E6%98%AF%E5%90%A6%E7%99%BB%E5%BD%95%22%3Atrue%2C%22UserID%22%3A%22412606846%40qq.com%22%7D%2C0%2C1533656307%2C0%2C1533656307%2Cnull%2C%22164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e%22%2C%221533654484%22%2C%22https%3A%2F%2Fmobile.umeng.com%2Fapps%22%2C%22mobile.umeng.com%22%5D; frontvar=siteShowHis%3Dopen%26siteListSortId%3D4%26cmenu%3D0; uc_session_id=78aac1e5-a957-4883-9eef-2d1c08894ba7; umplus_uc_token=1uiXjXjEYbHbEfj-IXGEmqw_42795acb5537441c8ba62e4e9942ebf0; umplus_uc_loginid=412606846%40qq.com; PHPSESSID=f14ut74kj2o5tr834fpc720fl5; CNZZDATA1258498910=4900034-1533654459-https%253A%252F%252Faccount.umeng.com%252F%7C1534913708; cn_1258498910_dplus=1%5B%7B%22userid%22%3A%22412606846%40qq.com%22%7D%2C0%2C1534916590%2C0%2C1534916590%2C%22%24direct%22%2C%22164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e%22%2C%221532913569%22%2C%22http%3A%2F%2Fweb.umeng.com%2Fmain.php%3Fc%3Duser%26a%3Dtip%26code%3D1000%26param3%3DaHR0cHM6Ly93ZWIudW1lbmcuY29tL21haW4ucGhwP2M9Y29udCZhPWZyYW1lJnNpdGVpZD0xMjczOTYzMjk4%26channel%3D%2523%2521%2F1529030080126%2Fcont%2Fpage%2F1%2F1273963298%2F2018-06-15%2F2018-06-15%22%2C%22web.umeng.com%22%5D; from=umeng; edtoken=cnzz_5b7cf7efb99be; isg=BFpa9II61Sl3kFmRYVxCVK5uqwC8I99vd6E47WTT0u2u1_sRTBlzdLEmo-NuRVb9; CNZZDATA30086426=cnzz_eid%3D1281187739-1533626752-%26ntime%3D1534914352; CNZZDATA33222=cnzz_eid%3D1207451176-1533625464-%26ntime%3D1534912198; _cnzz_CV30069868=%E6%98%AF%E5%90%A6%E7%99%BB%E5%BD%95%7C%E6%AD%A3%E5%B8%B8%E7%99%BB%E5%BD%95%7C1534945392604; CNZZDATA30069868=cnzz_eid%3D987871338-1533625979-%26ntime%3D1534915645; CNZZDATA30001831=cnzz_eid%3D75532440-1533624470-%26ntime%3D1534913755; cn_ea1523f470091651998a_dplus=%7B%22distinct_id%22%3A%20%22164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201534916637%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201534916637%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D%2C%22initial_view_time%22%3A%20%221533621991%22%2C%22initial_referrer%22%3A%20%22https%3A%2F%2Faccount.umeng.com%2F%22%2C%22initial_referrer_domain%22%3A%20%22account.umeng.com%22%7D"
COOKIES = {i.split('=')[0]: i.split('=')[1] for i in COOKIES.split('; ')}
# COOKIES = {
# 'PHPSESSID':'qomlg86kv2jriigumsrlp2bm20',
# 'UM_distinctid':'164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e',
# 'uc_session_id':'0b661a69-abdd-4815-9b65-424e116c86a8',
# 'cna':'LzXwE7Fb3SkCAd7JiwQV0nGW',
# 'umplus_uc_token':'1VUk5lTJ1n-jYEEwetrkMQw_d8178d18d35a46b783bb35850eae9b69',
# 'umplus_uc_loginid':'412606846%40qq.com',
# 'isg':'BJCQVXwn_3oNH6N_z0540iicYd4i8XWcsZOiQ4phVeu-xTBvMmiTM_f1mc2AFSx7',
# 'edtoken':'cnzz_5b694b3464c8b',
# 'CNZZDATA1258498910':'1886131770-1533622048-%7C1533622048',
# 'cn_ea1523f470091651998a_dplus':'%7B%22distinct_id%22%3A%20%22164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e%22%2C%22sp%22%3A%20%7B%7D%2C%22initial_view_time%22%3A%20%221533621991%22%2C%22initial_referrer%22%3A%20%22https%3A%2F%2Faccount.umeng.com%2F%22%2C%22initial_referrer_domain%22%3A%20%22account.umeng.com%22%7D',
# 'JSESSIONID':'B0E377A3209C1A6B4A2853B159ADE4DF',
# 'isg':'BGho17tVp2Id_YvnJ5YQ2sBEOVa6Oc2kiVvK-yKb7OPGfQjnyKAsK571cVUozYRz',
# 'cn_1258498910_dplus':'1%5B%7B%22userid%22%3A%22%22%7D%2C0%2C1533625114%2C0%2C1533625114%2C%22%24direct%22%2C%22164e90e72a7392-0a109216fa7ad8-47e1137-100200-164e90e72a835e%22%2C%221532913569%22%2C%22http%3A%2F%2Fweb.umeng.com%2Fmain.php%3Fc%3Duser%26a%3Dtip%26code%3D1000%26param3%3DaHR0cHM6Ly93ZWIudW1lbmcuY29tL21haW4ucGhwP2M9Y29udCZhPWZyYW1lJnNpdGVpZD0xMjczOTYzMjk4%26channel%3D%2523%2521%2F1529030080126%2Fcont%2Fpage%2F1%2F1273963298%2F2018-06-15%2F2018-06-15%22%2C%22web.umeng.com%22%5D'
# }

class Cookie:
    def __init__(self):
        self.password2 = '57a8e67e39df4eb091899f5f8ab0b6284641e1f3b9fbb58bbaf199477f3070f8b333a223e65e7a581e3f03e38a117ff756b6325fa087878e3b72c79af393b2267400a413e27b79dacc55d7804b3be8b9c3ddf90323c422b2528bc8bb042c31a4303dca0c5f7643ba6ff6422161d7670a0fa09a10552fdc5ea4c585e531662f24'
        self.loginId = '412606846@qq.com'
        self.password = 'weileFUMU1314'
        self.login_url = 'https://passport.alibaba.com/newlogin/login.do?fromSite=-2&appName=youmeng'
        self.heads = {
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            # 'content-type' : 'application/x-www-form-urlencoded; charset=UTF-8'
        }

    def get_cookie(self):
        r = s.post(self.login_url, headers=self.heads, data={'loginId':self.loginId,'password2':self.password2})
        data = r.text
        # print(data)
        for i in s.cookies:
            print(i.name,i.value)
        cookie1 = r.cookies
        for i in cookie1:
            print(i.name,i.value)
        # r = s.get('https://web.umeng.com/main.php?c=cont&a=page&ajax=module=summarysource|module=safeinfo|module=statistics_orderBy=pv_orderType=-1_dataType=source_currentPage=1_pageType=30&st=180620&et=180620')
        # print(r.text)
        return s

    # 用selenium部分更新cookies的方式
    def get_cookie_from_network(self):
        path = '../plugins/phantomjs/bin/phantomjs.exe'
        if not os.path.exists(path):
            path = 'plugins/phantomjs/bin/phantomjs.exe'
        driver = selenium.webdriver.PhantomJS(path)
        driver.get('https://passport.umeng.com/login')
        driver.switch_to.frame('alibaba-login-box')
        driver.find_element_by_id('fm-login-id').send_keys(self.loginId)
        driver.find_element_by_id('fm-login-password').send_keys(self.password)
        driver.find_element_by_id('fm-login-submit').click()
        cookies = {i['name']:i['value'] for i in driver.get_cookies()}
        # print(cookies)
        COOKIES.update(cookies)
        # self.heads.update({'Cookie':';'.join(['%s=%s'%(i,j) for i,j in COOKIES.items()])})
        # r = requests.get('https://web.umeng.com/main.php?c=cont&a=page&ajax=module=summarysource|module=safeinfo|module=statistics_orderBy=pv_orderType=-1_dataType=source_currentPage=1_pageType=30&st=180620&et=180620', headers=self.heads)
        # print(r.text)
        return COOKIES

if __name__ == '__main__':
    cookie = Cookie()
    print(cookie.get_cookie_from_network())
