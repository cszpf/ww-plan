# encoding=utf-8
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
    # def connect(self, db_name, _id='1'):
    #     # _id:'1'表示大学城数据库,'2'表示汪汪数据库
    #     db = eval("""MySQLdb.connect(self.ip{id}, self.user{id}, self.pwd{id},
    #     db_name, port=self.port{id}, charset='utf8')""".format(id=_id))
    #     return db
    def connect(self, db_name, _id='1'):
        # _id:'1'表示大学城数据库,'2'表示汪汪数据库
        if (db_name != ''):
            db = eval("""MySQLdb.connect(self.ip{id}, self.user{id}, self.pwd{id}, 
            db_name, port=self.port{id}, charset='utf8')""".format(id=_id))
        else:  # 需要跨数据库（fenqi、coupons）查询时则不指定数据库
            db = eval("""MySQLdb.connect(self.ip{id}, self.user{id}, self.pwd{id}, 
            port=self.port{id}, charset='utf8')""".format(id=_id))
        return db
    # 查询数据库
    def query(self, db_name, sql):
        db = self.connect(db_name)
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        return results
    # 将行政区code映射成name
    def region_code2name(self, code):
        sql = "SELECT region_name FROM micro_region WHERE region_code='{code}'".format(code=code)
        result = self.query(self.fenqi, sql)
        if result:
            return result[0][0]
        return None


class Export:
    def __init__(self):
        self.connect = Connect()
    # 实现门店流水表的在线生成
    def mdls(self, start_date, end_date, dir_name):
        # start_date:形如"2018-xx-xx"的str
        # end_date:形如"2018-xx-xx"的str
        # dir_name:存放门店流水表的目标文件夹
        columns = ['门店', '商户', '行政区', '微区域', '行业', '销售姓名', '运营姓名', '上线时间', '是否活跃', '是否沉默']
        all_data = []
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        for i in range((end_date - start_date).days):
            x = start_date + datetime.timedelta(i)
            columns.append(x.strftime("%y%m%d"))
        sql1 = """SELECT subbranch_id,subbranch_name,short_name,ADMIN_REGION_CODE,MICRO_REGION_CODE,
        merchant_type_name,SALE_NAME, OPERATOR_NAME,a.create_time 
        FROM subbranch a,merchant b, merchant_industry c 
        WHERE a.merchant_id=b.merchant_id AND b.merchant_type = c.merchant_type and a.state=2"""
        result = self.connect.query(self.connect.fenqi, sql1)
        for _sub in result:
            if _sub:
                data = [];
                data1 = {};
                _data = [];
                _sub = list(_sub)
                _sub[3] = self.connect.region_code2name(_sub[3]);
                _sub[4] = self.connect.region_code2name(_sub[4])
                _data.extend([_sub[i] for i in range(1, 9)])
                sql1 = """SELECT sum(amount),create_time FROM wechat_pay_log 
                WHERE subbranch_id='{}' AND type IN (2,3) AND state=2 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                sql2 = """SELECT sum(-amount),create_time FROM user_deposit_card_log 
                WHERE subbranch_id='{}' AND amount < 0 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                result1 = self.connect.query(self.connect.fenqi, sql1)  # 微信支付的消费结果
                result2 = self.connect.query(self.connect.fenqi, sql2)  # 储值卡支付的消费结果
                data.extend(result1)
                data.extend(result2)
                del (result1, result2)
                if data:  # 有消费记录
                    ddtgrq = _sub[-1].date() + datetime.timedelta(days=5)  # 到店推广日期
                    # 每一天门店流水
                    for _, __ in data:  # 消费金额和消费时间
                        data1.update({__.date(): data1.get(__.date(), 0) + _})
                    del (data)
                    max_date = max(data1.keys())
                    len_date = len(set(data1.keys()))
                    ifactive = True if len_date >= (
                        16 if (end_date - ddtgrq).days >= 30 else (end_date - ddtgrq).days // 2 + 1) else False
                    ifsilent = True if (end_date - max_date).days >= 15 else False
                else:  # 没有消费记录
                    ifactive = False;
                    ifsilent = True
                _data.extend([ifactive, ifsilent])
                for i in range((end_date - start_date).days):
                    x = start_date + datetime.timedelta(i)
                    _data.append(data1.get(x, 0))
            all_data.append(_data)
        # print(all_data)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data, columns=columns)
        df.to_csv(os.path.join(dir_name, 'mdls.csv'), index=False, encoding='gbk', sep=',')
        return all_data

      # 实现门店流水占比表的在线生成
    def mdlszb(self, start_date, end_date, dir_name):
        columns = ['门店', '商户', '行政区', '微区域', '行业', '销售姓名', '运营姓名', '上线时间', '是否活跃', '是否沉默']
        all_data = []
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        for i in range((end_date - start_date).days):
            x = start_date + datetime.timedelta(i)
            columns.append(x.strftime("%y%m%d"))
        sql1 = """SELECT subbranch_id,subbranch_name,short_name,ADMIN_REGION_CODE,MICRO_REGION_CODE,
        merchant_type_name,SALE_NAME, OPERATOR_NAME,a.create_time,AVERAGE_ASSESS_INCOME 
        FROM subbranch a,merchant b, merchant_industry c 
        WHERE a.merchant_id=b.merchant_id AND b.merchant_type = c.merchant_type """
        result = self.connect.query(self.connect.fenqi, sql1)
        for _sub in result:
            if _sub:#如果有值的话
                _sub = list(_sub)#把一行有逗号的数据变成列表，把三四行政区code映射成name
                _sub[3] = self.connect.region_code2name(_sub[3]);#行政区
                _sub[4] = self.connect.region_code2name(_sub[4])#微区域
                data = [];#用来存放每一笔的消费（消费+创建时间）
                data1 = {};#用来存每一个门店的消费加创建时间（每一天的流水，按时间天数为键）
                _data = []#用来存放一行数据
                _data.extend([_sub[i] for i in range(1, 9)])#把result每一行的数据_sub放入_data列表中
                sql1 = """SELECT sum(amount),create_time FROM wechat_pay_log 
                WHERE subbranch_id='{}' AND type IN (2,3) AND state=2 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])
                sql2 = """SELECT sum(-amount),create_time FROM user_deposit_card_log 
                WHERE subbranch_id='{}' AND amount < 0 GROUP BY create_time 
                ORDER BY create_time """.format(_sub[0])#因为result每一行的数据_sub都是一个门店
                result1 = self.connect.query(self.connect.fenqi, sql1)  # 微信支付的消费结果
                result2 = self.connect.query(self.connect.fenqi, sql2)  # 储值卡支付的消费结果
                data.extend(result1)
                data.extend(result2)#用data记录每一笔的消费（消费+创建时间）
                del (result1, result2)
                if data:  # 有消费记录
                    ddtgrq = _sub[8].date() + datetime.timedelta(days=5)  # 到店推广日期
                    # 每一天门店流水
                    for _, __ in data:  # 在data1里面存入这一个门店的消费金额和消费时间
                        data1.update({__.date(): data1.get(__.date(), 0) + _})
                    del (data)
                    max_date = max(data1.keys())#最大时间
                    len_date = len(set(data1.keys()))#时间长度
                    ifactive = True if len_date >= (
                        16 if (end_date - ddtgrq).days >= 30 else (end_date - ddtgrq).days // 2 + 1) else False
                    ifsilent = True if (end_date - max_date).days >= 15 else False
                else:  # 没有消费记录
                    ifactive = False;
                    ifsilent = True
                _data.extend([ifactive, ifsilent])

                for i in range((end_date - start_date).days):
                    x = start_date + datetime.timedelta(i)
                    try:
                        _zb = round(float(data1.get(x, 0)) / float(_sub[-1]), 3)
                    except:
                        _zb = 0
                    finally:
                        _data.append(_zb)
            all_data.append(_data)
        print(all_data)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data, columns=columns)
        df.to_csv(os.path.join(dir_name, 'mdlszb.csv'), index=False, encoding='gbk', sep=',')
        return all_data

    def mdpm(self, start_date, end_date, dir_name):
        indexs = []
        indexs.extend(['指标', 'TOP10活跃门店名称', 'TOP10活跃门店活跃天数', 'TOP10流水门店名称', 'TP10流水门店流水'
                      , 'TOP10用券次数门店名称','TOP10用券次数门店总用券次数', 'TOP10用券次数门店客单价',
                       'TOP10客单价门店名称', 'TOP10客单价门店客单价'])
        all_data = []
        top = ['TOP1', 'TOP2', 'TOP3', 'TOP4', 'TOP5', 'TOP6', 'TOP7', 'TOP8', 'TOP9', 'TOP10', 'TOP10门店流水总比重']
        all_data.append(top)
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        sql = """SELECT subbranch_id,subbranch_name,create_time,state
                FROM subbranch 
                where create_time is not null and state=2"""
        result = self.connect.query(self.connect.fenqi, sql)
        d1 = {}  # 用来存所有的门店和所有门店的总流水
        d2 = {}#用来存放所有门店的活跃（流水）天数
        d1count = {}  # d1count统计的是每个门店的消费笔数
        for _sub in result:  # 遍历所有门店
            huoyue = {}  # 用来存放活消费时间+活跃天数
            sqlwechat = """SELECT sum(amount),create_time FROM wechat_pay_log 
                           WHERE subbranch_id='{0}' AND type IN (2,3) AND state=2 
                           AND create_time between '{1}' and '{2}'
                           GROUP BY create_time 
                           ORDER BY create_time """.format(_sub[0], start_date,end_date)
            sqldeposit = """SELECT sum(-amount),create_time FROM user_deposit_card_log 
                            WHERE subbranch_id='{0}' AND amount < 0 
                            AND create_time between '{1}' and '{2}'
                            GROUP BY create_time  
                            ORDER BY create_time """.format(_sub[0], start_date,end_date)
            resultdeposit = self.connect.query(self.connect.fenqi, sqlwechat)  # 遍历每个门店的微信流水
            resultwechat = self.connect.query(self.connect.fenqi, sqldeposit)  # 遍历每个门店的储值卡流水
            moneydata = [];count1 = 0
            moneydata.extend(resultdeposit)
            moneydata.extend(resultwechat)
            del (resultwechat, resultdeposit)
            for i in moneydata:
                if i:
                    d1.update({_sub[1]: d1.get(_sub[1], 0) + i[0]})  # 所以d1存的是每个门店的名字和总流水
                    count1 = count1 + 1
                    huoyue.update({i[1].date():huoyue.get(i[1].date,0)+i[0]})
            d1count.update({_sub[1]: d1count.get(_sub[1], 0) + count1})  # d1count统计的是每个门店的消费笔数
            len_date = len(set(huoyue.keys()))  # 时间长度
            if len_date:
                d2.update({_sub[1]:d2.get(_sub[0],0)+len_date})

        # 计算门店总流水
        totalamount=0
        for name,money in d1.items():
                totalamount=totalamount+money

        #统计TOP10活跃门店名称
        dd2 = sorted(d2.items(), key=lambda item: item[1], reverse=True)  # 按照流水金额排序得到top10流水
        hylie1=[];hylie2=[];hytopls=0;hycount=1
        for name, day in dd2:
                if hycount <= 10:
                    hylie1.append(name)  # 门店名称
                    hylie2.append(day)  # 活跃天数
                    hytopls = hytopls + d1.get(name, 0)  # TOP10流水
                    hycount = hycount + 1
        if hycount <= 10:
            for i in range(hycount, 11):
                hylie1.append('-')
                hylie2.append('-')
        hyzb = round(hytopls / totalamount, 3)  # 流水占比
        hylie1.append(hyzb)
        all_data.append(hylie1)
        all_data.append(hylie2)

        #统计TOP10流水门店名称
        dd1 = sorted(d1.items(), key=lambda item: item[1], reverse=True)  # 按照流水金额排序得到top10流水
        lslie1 = [];lslie2 = [];lstopls = 0;lscount = 1
        for name, amount in dd1:
            if lscount <= 10:
                lslie1.append(name)  # 门店名称
                lslie2.append(amount)  # 流水
                lstopls = lstopls + d1.get(name, 0)  # TOP10流水
                lscount = lscount + 1
        if lscount <= 10:
            for i in range(lscount, 11):
                lslie1.append('-')
                lslie2.append('-')
        lszb = round(lstopls / totalamount, 3)  # 流水占比
        lslie1.append(lszb)
        all_data.append(lslie1)
        all_data.append(lslie2)

        #TOP10用券次数门店名称,直接看券的日志，找到每一笔微信和储值卡消费是由哪家店使用的
        sql3deposit = """SELECT c.subbranch_name,-b.amount
                        FROM {0}.coupons_log a,{1}.user_deposit_card_log b,{1}.subbranch c
                        WHERE a.user_deposit_card_log_id=b.user_deposit_card_log_id and b.subbranch_id=c.subbranch_id
                        and a.create_time between '{2}' and '{3}'""".format(self.connect.coupons,
                        self.connect.fenqi,start_date, end_date)
        sql3wechat = """SELECT c.subbranch_name,b.amount 
                        FROM {0}.coupons_log a,{1}.wechat_pay_log b,{1}.subbranch c
                        WHERE a.wechat_pay_log_id=b.wechat_pay_log_id and b.subbranch_id=c.subbranch_id
                        and a.create_time between '{2}' and '{3}'""".format(self.connect.coupons,
                        self.connect.fenqi,start_date, end_date)
        result3deposit = self.connect.query('', sql3deposit)  # 微信用券日志
        result3wechat = self.connect.query('', sql3wechat)  # 储值卡用券日志
        data = [];data1 = {};data2 = {}
        data.extend(result3deposit)
        data.extend(result3wechat)
        del (result3deposit, result3wechat)
        for name, amount in data:
            data1.update({name: data1.get(name, 0) + amount})  # 门店和金额
            data2.update({name: data2.get(name, 0) + 1})  # 门店和用券次数
        data3 = sorted(data2.items(), key=lambda item: item[1], reverse=True)  # 按照次数排序
        yqlie1=[];yqlie2=[];yqlie3=[];yqcount=1;yqtopls=0
        for i in data3:
            if i:
                if yqcount <=10:
                    yqlie1.append(i[0])  # 门店名称
                    yqlie2.append(data2[i[0]])  # 门店用券次数
                    yqlie3.append(round(float(data1[i[0]]) / float(i[1]), 2))  # 客单价
                    yqtopls = yqtopls + d1.get(i[0], 0)  # TOP10流水
                    yqcount = yqcount + 1
        if yqcount <=10:
            for i in range(yqcount, 11):
                yqlie1.append('-')
                yqlie2.append('-')
                yqlie3.append('-')
        zb3 = round(yqtopls / totalamount, 3)  # 流水占比
        yqlie1.append(zb3)
        all_data.append(yqlie1)
        all_data.append(yqlie2)
        all_data.append(yqlie3)

        #TOP10客单价门店名称
        kdj = {}  # 用来存每个门店的名称和客单价
        for name,amount in d1.items():
            if amount:
                kdj.update({name: round(d1.get(name, 0) / d1count.get(name), 2)})  # 保留两位小数
        kdj1 = sorted(kdj.items(), key=lambda item: item[1], reverse=True)
        kdjlie1=[];kdjlie2=[];kdjcount=1;kdjtopls=0
        for i in kdj1:
            if kdjcount <=10:
                kdjlie1.append(i[0])  # 门店名称
                kdjlie2.append(i[1])  # 门店客单价
                kdjtopls = kdjtopls + d1.get(i[0], 0)  # TOP10流水
                kdjcount = kdjcount + 1
        if kdjcount <=10:
            for i in range(kdjcount, 11):
                kdjlie1.append('-')
                kdjlie2.append('-')
        zb4 = round(kdjtopls / totalamount, 3)  # 流水占比
        kdjlie1.append(zb4)
        all_data.append(kdjlie1)
        all_data.append(kdjlie2)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data,index=indexs)
        df = df.stack().unstack(0)
        df.to_csv(os.path.join(dir_name, 'mdpm.csv'), index=False, encoding='gbk', sep=',')

def main():
    export = Export()
    #export.mdlszb('2018-6-1', '2018-6-3', r'\Users\qiqi\Desktop')
    #export.shqxq('2018-1-03','2018-7-1', r'\Users\qiqi\Desktop')
    export.mdpm('2018-1-03', '2018-7-30', r'\Users\qiqi\Desktop')
if __name__ == '__main__':
    main()