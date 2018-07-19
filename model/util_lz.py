#encoding=utf-8
import MySQLdb
import datetime
import os
import pandas as pd
cwd = os.getcwd()

class Connect:
    def __init__(self):
        self.fenqi, self.coupons = 'fenqi', 'coupons'
        # 大学城数据库
        self.ip1, self.user1, self.pwd1, self.port1 = '183.3.143.131', 'root', 'Wangwang@scut123', 552
        # 汪汪本地数据库
        self.ip2, self.user2, self.pwd2, self.port2 = '192.168.1.14', 'root', '123456', 8306
    
    # 数据库连接
    def connect(self, db_name, _id='1'):
        # _id:'1'表示大学城数据库,'2'表示汪汪数据库
        db = eval("""MySQLdb.connect(self.ip{id}, self.user{id}, self.pwd{id}, 
        db_name, port=self.port{id}, charset='utf8')""".format(id=_id))
        return db

    # 查询数据库
    def query(self, db_name, sql):
        db = self.connect(db_name)
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        return results
    
    # 将区域code映射成name
    def region_code2name(self,code):
        sql = "SELECT region_name FROM micro_region WHERE region_code='{code}'".format(code = code)
        result = self.query(self.fenqi,sql)
        if result:
            return result[0][0]
        return None

    # 将门店ID映射成商户ID
    def subid2merid(self, subid):
        sql = """SELECT a.merchant_id FROM merchant a, subbranch b WHERE a.merchant_id = b.merchant_id AND b.subbranch_id = '{subid}'""".format(subid = subid)
        result = self.query(self.fenqi, sql)
        if result:
            return result[0][0]
        return None

    #将商店ID映射成商户简称
    def merid2shortname(self, merid):
        sql = """SELECT merchant_id, short_name FROM merchant WHERE merchant_id = '{merid}'""".format(merid = merid)
        result = self.query(self.fenqi, sql)
        if result:
            return result[0][1]
        return None



class Export:
    def __init__(self):
        self.connect = Connect()
    
    # 实现门店流水表的在线生成
    def mdls(self, start_date, end_date, dir_name):
        # start_date:形如"2018-xx-xx"的str
        # end_date:形如"2018-xx-xx"的str
        # dir_name:存放门店流水表的目标文件夹
        columns = ['门店','商户','行政区','微区域','行业','销售姓名','运营姓名','上线时间','是否活跃','是否沉默']
        all_data = []
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        for i in range((end_date-start_date).days):
            x = start_date + datetime.timedelta(i)
            columns.append(x.strftime("%y%m%d"))
        sql1 = """SELECT subbranch_id,subbranch_name,short_name,ADMIN_REGION_CODE,MICRO_REGION_CODE,
        merchant_type_name,SALE_NAME, OPERATOR_NAME,a.create_time 
        FROM subbranch a,merchant b, merchant_industry c 
        WHERE a.merchant_id=b.merchant_id AND b.merchant_type = c.merchant_type """
        result = self.connect.query(self.connect.fenqi, sql1)
        for _sub in result:
            if _sub:
                data = []; data1 = {}; _data = []; _sub=list(_sub)
                _sub[3] = self.connect.region_code2name(_sub[3]);_sub[4] = self.connect.region_code2name(_sub[4])
                _data.extend([_sub[i] for i in range(1,9)])
                sql1 = """SELECT sum(amount),create_time FROM wechat_pay_log 
                WHERE subbranch_id='{}' AND type IN (2,3) AND state=2 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                sql2 = """SELECT sum(-amount),create_time FROM user_deposit_card_log 
                WHERE subbranch_id='{}' AND amount < 0 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                result1 = self.connect.query(self.connect.fenqi, sql1)#微信支付的消费结果
                result2 = self.connect.query(self.connect.fenqi, sql2)#储值卡支付的消费结果
                data.extend(result1)
                data.extend(result2)
                del(result1,result2)
                if data:#有消费记录
                    sxrq = _sub[-1].date() if _sub[-1] != '' else datetime.date(2017,1,1)
                    # 每一天门店流水
                    for _,__ in data:#消费金额和消费时间
                        data1.update({__.date():data1.get(__.date(),0)+_})
                    del(data)
                    max_date = max(data1.keys())
                    len_date = len(set(data1.keys()))
                    ifactive = True if len_date >= (16 if (end_date-sxrq).days >= 30 else (end_date-sxrq).days//2 + 1) else False
                    ifsilent = True if (end_date - max_date).days >= 15 else False
                else:#没有消费记录
                    ifactive = False; ifsilent = True
                _data.extend([ifactive, ifsilent])
                for i in range((end_date-start_date).days):
                    x = start_date + datetime.timedelta(i)
                    _data.append(data1.get(x,0))
            all_data.append(_data)
        #print(all_data)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data,columns=columns)
        df.to_csv(os.path.join(dir_name,'mdls.csv'),index=False,encoding='gbk',sep=',')
        return all_data

        # 实现门店流水占比表的在线生成
    def mdlszb(self, start_date, end_date, dir_name):
        # start_date:形如"2018-xx-xx"的str
        # end_date:形如"2018-xx-xx"的str
        # dir_name:存放门店流水占比表的目标文件夹
        columns = ['门店','商户','行政区','微区域','行业','销售姓名','运营姓名','上线时间','是否活跃','是否沉默']
        all_data = []
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        for i in range((end_date-start_date).days):
            x = start_date + datetime.timedelta(i)
            columns.append(x.strftime("%y%m%d"))
        sql1 = """SELECT subbranch_id,subbranch_name,short_name,ADMIN_REGION_CODE,MICRO_REGION_CODE,
        merchant_type_name,SALE_NAME, OPERATOR_NAME,a.create_time,AVERAGE_ASSESS_INCOME 
        FROM subbranch a,merchant b, merchant_industry c 
        WHERE a.merchant_id=b.merchant_id AND b.merchant_type = c.merchant_type """
        result = self.connect.query(self.connect.fenqi, sql1)
        for _sub in result:
            if _sub:
                _sub = list(_sub)
                _sub[3] = self.connect.region_code2name(_sub[3]);_sub[4] = self.connect.region_code2name(_sub[4])
                data = []; data1 = {}; _data = []
                _data.extend([_sub[i] for i in range(1,9)])
                sql1 = """SELECT sum(amount),create_time FROM wechat_pay_log 
                WHERE subbranch_id='{}' AND type IN (2,3) AND state=2 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                sql2 = """SELECT sum(-amount),create_time FROM user_deposit_card_log 
                WHERE subbranch_id='{}' AND amount < 0 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                result1 = self.connect.query(self.connect.fenqi, sql1)#微信支付的消费结果
                result2 = self.connect.query(self.connect.fenqi, sql2)#储值卡支付的消费结果
                data.extend(result1)
                data.extend(result2)
                del(result1,result2)
                if data:#有消费记录
                    sxrq = _sub[-2].date() if _sub[-2] != '' else datetime.date(2017,1,1)
                    # 每一天门店流水
                    for _,__ in data:#消费金额和消费时间
                        data1.update({__.date():data1.get(__.date(),0)+_})
                    del(data)
                    max_date = max(data1.keys())
                    len_date = len(set(data1.keys()))
                    ifactive = True if len_date >= (16 if (end_date-sxrq).days >= 30 else (end_date-sxrq).days//2 + 1) else False
                    ifsilent = True if (end_date - max_date).days >= 15 else False
                else:#没有消费记录
                    ifactive = False; ifsilent = True
                _data.extend([ifactive, ifsilent])
                for i in range((end_date-start_date).days):
                    x = start_date + datetime.timedelta(i)
                    try:
                        _zb = round(float(data1.get(x,0))/float(_sub[-1]),3)
                    except:
                        _zb = 0
                    finally:
                        _data.append(_zb)
            all_data.append(_data)
        # print(all_data)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data,columns=columns)
        df.to_csv(os.path.join(dir_name,'mdlszb.csv'),index=False,encoding='gbk',sep=',')
        return all_data

    # 实现沉默门店表的在线生成
    def cmmd(self, start_date, end_date, dir_name):
        # start_date:形如"2018-xx-xx"的str
        # end_date:形如"2018-xx-xx"的str
        # dir_name:存放沉默门店表的目标文件夹
        indexs = []
        all_data = []
        subdict = {}
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        for i in range((end_date-start_date).days):
            x = start_date + datetime.timedelta(i)
            indexs.append(x.strftime("%y%m%d"))
        sql = """SELECT subbranch_id,subbranch_name,a.create_time,short_name,merchant_type 
        FROM subbranch a,merchant b 
        WHERE a.merchant_id=b.merchant_id """
        result = self.connect.query(self.connect.fenqi, sql)
        for _sub in result:
            if _sub:
                data = []; 
                sql1 = """SELECT sum(amount),create_time FROM wechat_pay_log 
                WHERE subbranch_id='{}' AND type IN (2,3) AND state = 2 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                sql2 = """SELECT sum(-amount),create_time FROM user_deposit_card_log 
                WHERE subbranch_id='{}' AND amount < 0 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                result1 = self.connect.query(self.connect.fenqi, sql1)#微信支付的消费结果
                result2 = self.connect.query(self.connect.fenqi, sql2)#储值卡支付的消费结果
                data.extend(result1)
                data.extend(result2)
                del(result1,result2)
                subdict[_sub[0]] = data
        for i in range((end_date-start_date).days):
            x = start_date + datetime.timedelta(i)
            _data = []
            for _sub in result:
                if _sub:
                    datelist = []; 
                    data = subdict[_sub[0]]
                    if data:
                        # 每一天门店流水
                        for _,__ in data:
                            datelist.append(__.date())
                        max_date = max(datelist)
                        ifsilent = True if (x - max_date).days >= 15 else False
                    else:
                        ifsilent = True
                    if ifsilent:
                        _data.append(_sub[1])
            all_data.append(_data)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data,index = indexs)
        df = df.stack().unstack(0)
        df.to_csv(os.path.join(dir_name,'cmmd.csv'),index=False,encoding='gbk', sep=',')
        return all_data

    # 实现活跃门店表的在线生成
    def hymd(self, start_date, end_date, dir_name):
        # start_date:形如"2018-xx-xx"的str
        # end_date:形如"2018-xx-xx"的str
        # dir_name:存放活跃门店表的目标文件夹
        indexs = []
        all_data = []
        subdict = {}
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        for i in range((end_date-start_date).days):
            x = start_date + datetime.timedelta(i)
            indexs.append(x.strftime("%y%m%d"))
        sql1 = """SELECT subbranch_id,subbranch_name,a.create_time,short_name,merchant_type 
        FROM subbranch a,merchant b 
        WHERE a.merchant_id=b.merchant_id """
        result = self.connect.query(self.connect.fenqi, sql1)
        for _sub in result:
            if _sub:
                data = [];
                sql1 = """SELECT sum(amount),create_time FROM wechat_pay_log 
                WHERE subbranch_id='{}' AND type IN (2,3) AND state = 2 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                sql2 = """SELECT sum(-amount),create_time FROM user_deposit_card_log 
                WHERE subbranch_id='{}' AND amount < 0 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                result1 = self.connect.query(self.connect.fenqi, sql1)#微信支付的消费结果
                result2 = self.connect.query(self.connect.fenqi, sql2)#储值卡支付的消费结果
                data.extend(result1)
                data.extend(result2)
                del(result1,result2)
                subdict[_sub[0]] = data
        for i in range((end_date-start_date).days):
            x = start_date + datetime.timedelta(i)
            _data = []
            for _sub in result:
                if _sub:
                    datelist = []; 
                    data = subdict[_sub[0]]
                    if data:
                        sxrq = _sub[-3].date() if _sub[-3] != '' else datetime.date(2017,1,1)
                        for _,__ in data:
                            datelist.append(__.date())
                        max_date = max(datelist)
                        len_date = len(set(datelist))
                        ifactive = True if len_date >= (16 if (x-sxrq).days >= 30 else (x-sxrq).days//2 + 1) else False
                    else:
                        ifactive = False
                    if ifactive:
                        _data.append(_sub[1])
            all_data.append(_data)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data,index = indexs)
        df = df.stack().unstack(0)
        df.to_csv(os.path.join(dir_name,'hymd.csv'),index=False,encoding='gbk', sep=',')
        return all_data    

    # 实现异动商户表的在线生成
    def ydsh(self, start_date, end_date, dir_name):
        # start_date:形如"2018-xx-xx"的str
        # end_date:形如"2018-xx-xx"的str
        # dir_name:存放异动商户表的目标文件夹
        indexs = []
        data = []
        all_data = []
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        for i in range((end_date-start_date).days):
            x = start_date + datetime.timedelta(i)
            indexs.append(x.strftime("%y%m%d"))
        sql1 = """SELECT a.merchant_id, short_name, update_time
        FROM fenqi.merchant a, coupons.coupons_config b
        WHERE a.merchant_id = b.merchant_id"""
        sql2 = """SELECT a.merchant_id, short_name, b.create_time
        FROM merchant a, merchant_product b
        WHERE a.merchant_id = b.merchant_id""" 
        result1 = self.connect.query(self.connect.fenqi, sql1)
        result2 = self.connect.query(self.connect.fenqi, sql2)
        data.extend(result1)
        data.extend(result2)
        del(result1, result2)
        for i in range((end_date-start_date).days):
            x = start_date + datetime.timedelta(i)
            _data = set()
            for _sub in data: 
                if(_sub[-1] and _sub[-1].date() == x):
                    _data.add(_sub[1])
            all_data.append(list(_data))
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data,index = indexs)
        df = df.stack().unstack(0)
        df.to_csv(os.path.join(dir_name,'ydsh.csv'),index=False,encoding='gbk', sep=',')
        return all_data 

    # 实现流失商户表的在线生成
    def lssh(self, start_date, end_date, dir_name):
        # start_date:形如"2018-xx-xx"的str
        # end_date:形如"2018-xx-xx"的str
        # dir_name:存放流失商户表的目标文件夹
        indexs = []
        all_data = []
        subdict = {}
        
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        for i in range((end_date-start_date).days):
            x = start_date + datetime.timedelta(i)
            indexs.append(x.strftime("%y%m%d"))
        sql = """SELECT subbranch_id,subbranch_name,a.create_time,short_name,merchant_type 
        FROM subbranch a,merchant b 
        WHERE a.merchant_id=b.merchant_id """
        result = self.connect.query(self.connect.fenqi, sql)
        for _sub in result:
            if _sub:
                data = []; 
                sql1 = """SELECT sum(amount),create_time FROM wechat_pay_log 
                WHERE subbranch_id='{}' AND type IN (2,3) AND state = 2 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                sql2 = """SELECT sum(-amount),create_time FROM user_deposit_card_log 
                WHERE subbranch_id='{}' AND amount < 0 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                result1 = self.connect.query(self.connect.fenqi, sql1)#微信支付的消费结果
                result2 = self.connect.query(self.connect.fenqi, sql2)#储值卡支付的消费结果
                data.extend(result1)
                data.extend(result2)
                del(result1,result2)
                subdict[_sub[0]] = data

        for i in range((end_date-start_date).days):
            x = start_date + datetime.timedelta(i)
            #指定日期前15天没有流水的商户
            tempdata = []
            _data = set()
            merdict = {}
            for _sub in result:
                if _sub:
                    datelist = []; 
                    data = subdict[_sub[0]]
                    if data:
                        for _,__ in data:
                            datelist.append(__.date())
                        max_date = max(datelist)
                        ifsilent = True if (x - max_date).days >= 15 else False
                    else:
                        ifsilent = True
                    if ifsilent:
                        merid = self.connect.subid2merid(_sub[0])
                        if not merid in merdict:
                            merdict[merid] = 0
                        merdict[merid] += 1
            for merid in merdict:
                sql3 = """SELECT a.merchant_id,merchant_name, subbranch_id, subbranch_name 
                FROM merchant a, subbranch b
                WHERE a.merchant_id = b.merchant_id AND a.merchant_id = '{}'""".format(merid)
                result3 = self.connect.query(self.connect.fenqi, sql3)
                if(len(result3) == merdict[merid]):
                    tempdata.append(merid)
            #后台优惠券全部下架的商户
            for j in tempdata:
                sql4 = """SELECT merchant_id, subbranch_id
                FROM coupons_config
                WHERE merchant_id = '{}' AND (status = 1 OR status = 2)""".format(j)
                result4 = self.connect.query(self.connect.coupons, sql4)
                if(len(result4) == 0):
                    _data.add(self.connect.merid2shortname(j))
            all_data.append(list(_data))  

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data,index = indexs)
        df = df.stack().unstack(0)
        df.to_csv(os.path.join(dir_name,'lssh.csv'),index=False,encoding='gbk', sep=',')
        return all_data

    # 实现门店汇总表的在线生成
    def mdhz(self, start_date, end_date, dir_name):
        # start_date:形如"2018-xx-xx"的str
        # end_date:形如"2018-xx-xx"的str
        # dir_name:存放门店汇总表的目标文件夹
        indexs = []
        columns = ['新增门店数', '累计门店数', '累计评估收入', '累计运营流水', '累计流水占比', '户均评估收入', 
        '户均运营流水', '户均流水占比', '活跃门店数量', '活跃门店占比', '沉默门店数量', '异动商户数量', '流失商户数量']
        all_data = []
        subdict = {}
        hymd_data = self.hymd(start_date, end_date, dir_name)
        cmmd_data = self.cmmd(start_date, end_date, dir_name)
        ydsh_data = self.ydsh(start_date, end_date, dir_name)
        lssh_data = self.lssh(start_date, end_date, dir_name)
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        for i in range((end_date-start_date).days):
            x = start_date + datetime.timedelta(i)
            indexs.append(x.strftime("%y%m%d"))
        sql = """SELECT subbranch_id,subbranch_name,a.create_time,short_name,merchant_type 
        FROM subbranch a,merchant b 
        WHERE a.merchant_id=b.merchant_id """
        result = self.connect.query(self.connect.fenqi, sql)
        for _sub in result:
            if _sub:
                data = []; 
                sql1 = """SELECT sum(amount),create_time FROM wechat_pay_log 
                WHERE subbranch_id='{}' AND type IN (2,3) AND state = 2 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                sql2 = """SELECT sum(-amount),create_time FROM user_deposit_card_log 
                WHERE subbranch_id='{}' GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                result1 = self.connect.query(self.connect.fenqi, sql1)#微信支付的消费结果
                result2 = self.connect.query(self.connect.fenqi, sql2)#储值卡支付的消费结果
                data.extend(result1)
                data.extend(result2)
                del(result1,result2)
                subdict[_sub[0]] = data
        for i in range((end_date-start_date).days):
            x = start_date + datetime.timedelta(i)
            sql1 = """SELECT subbranch_id, create_time, average_assess_income FROM subbranch ORDER BY create_time"""
            result1 = self.connect.query(self.connect.fenqi, sql1)
            _data = []
            newly_sub = accum_sub = 0
            accum_assess_income = accum_yyls = 0.0
            for _sub1 in result1:
                if _sub1[1]:
                    if _sub1[1].date() <= x:
                        accum_sub += 1
                        if _sub1[1].date() == x:
                            newly_sub += 1
                        if _sub1[2]:
                            accum_assess_income += float(_sub1[2])
            _data.extend([newly_sub, accum_sub,accum_assess_income])
            for _sub in result:
                if _sub:
                    data = subdict[_sub[0]]
                    data1 = {}            
                    if data:#有消费记录
                        # 每一天门店流水
                        for _,__ in data:#消费金额和消费时间
                            data1.update({__.date():data1.get(__.date(),0)+_})
                    accum_yyls += float(data1.get(x, 0))
            try:
                accum_lszb = str(round(float(accum_yyls)/float(accum_assess_income),3)*100) + '%'
            except:
                accum_lszb = 0
            try:
                aver_house_lszb = str(round(float(aver_house_yyls)/float(aver_house_access_income),3)*100) + '%'
            except:
                aver_house_lszb = 0
            aver_house_access_income = accum_assess_income/accum_sub
            aver_house_yyls = accum_yyls/accum_sub
            _data.extend([accum_yyls, accum_lszb, aver_house_access_income, aver_house_yyls, aver_house_lszb])
            
            hymd_num = len(hymd_data[i])
            hymd_zb = str(round(float(hymd_num)/float(accum_sub),3)*100) + '%'
            cmmd_num = len(cmmd_data[i])
            ydsh_num = len(ydsh_data[i])
            lssh_num = len(lssh_data[i])
            _data.extend([hymd_num, hymd_zb, cmmd_num, ydsh_num, lssh_num])
            all_data.append(_data)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data,index = indexs, columns = pd.Index(columns, name = '指标'))
        df = df.stack().unstack(0)
        df.to_csv(os.path.join(dir_name,'mdhz.csv'), encoding='gbk', sep=',')
        return all_data 



def main():
    export = Export()
    #export.mdls('2018-6-19','2018-6-30','./')
    #export.mdlszb('2018-6-1','2018-6-4','./')
    #export.cmmd('2018-6-1', '2018-6-10', './')
    #export.hymd('2018-6-1','2018-6-10','./')
    #export.ydsh('2018-6-1','2018-6-10','./')
    #export.lssh('2018-6-1','2018-6-10','./')
    export.mdhz('2018-6-1','2018-6-10','./')
if __name__ == '__main__':
    main()