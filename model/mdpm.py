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
        WHERE a.merchant_id=b.merchant_id AND b.merchant_type = c.merchant_type """
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
        indexs.extend(['指标','TOP10活跃门店名称','TOP10活跃门店活跃天数','TOP10流水门店名称','TP10流水门店流水','TOP10用券次数门店名称',
                       'TOP10用券次数门店总用券次数','TOP10用券次数门店客单价','TOP10客单价门店名称','TOP10客单价门店客单价'])
        all_data = []
        top=['TOP1','TOP2','TOP3','TOP4','TOP5','TOP6','TOP7','TOP8','TOP9','TOP10','TOP10门店流水总比重']
        all_data.append(top)
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # 得到TOP10门店流水名称和流水
        sql = """SELECT subbranch_id,subbranch_name,create_time FROM subbranch where create_time is not null"""  # 找到所有门店名称和id
        result = self.connect.query(self.connect.fenqi, sql)
        d1 = {}  # 用来存所有的门店和所有门店的总流水
        d1count = {}  # d1count统计的是每个门店的消费笔数
        for _sub in result:  # 遍历所有门店
            sql2wechat = """SELECT sum(amount),create_time FROM wechat_pay_log 
                                                    WHERE subbranch_id='{0}' AND type IN (2,3) AND state=2 
                                                    AND create_time between '{1}' and '{2}'
                                                    GROUP BY create_time 
                                                    ORDER BY create_time """.format(_sub[0], start_date, end_date)
            sql2deposit = """SELECT sum(-amount),create_time FROM user_deposit_card_log 
                                                    WHERE subbranch_id='{0}' AND amount < 0 
                                                    AND create_time between '{1}' and '{2}'
                                                    GROUP BY create_time  
                                                    ORDER BY create_time """.format(_sub[0], start_date,
                                                                                    end_date)  # 因为result每一行的数据_sub都是一个门店
            result2deposit = self.connect.query(self.connect.fenqi, sql2deposit)  # 遍历每个门店的储值卡流水
            result2wechat = self.connect.query(self.connect.fenqi, sql2wechat)  # 遍历每个门店的微信流水
            money2 = [];count1 = 0
            money2.extend(result2deposit)
            money2.extend(result2wechat)
            del (result2deposit, result2wechat)
            for i in money2:
                if i:
                    d1.update({_sub[1]: d1.get(_sub[1], 0) + i[0]})  # 所以d1存的是每个门店的名字和总流水
                    count1 = count1 + 1
            d1count.update({_sub[1]: d1count.get(_sub[1], 0) + count1})  # d1count统计的是每个门店的消费笔数

        #得到TOP10活跃门店名称和活跃天数
        huoyue={}#活跃门店名称和活跃天数
        for _sub in result:#遍历门店
            if _sub:
                money = [];# 用money记录这家门店每一笔的消费（消费+创建时间）
                money_data = {}#将得到的消费结果按天存放
                sql1wechat = """SELECT sum(amount),create_time FROM wechat_pay_log 
                                WHERE subbranch_id='{}' AND type IN (2,3) AND state=2 GROUP BY create_time 
                                ORDER BY create_time """.format(_sub[0])
                sql1deposit = """SELECT sum(-amount),create_time FROM user_deposit_card_log 
                                WHERE subbranch_id='{}' AND amount < 0 GROUP BY create_time  
                                ORDER BY create_time """.format(_sub[0])
                cjrq = datetime.datetime.strptime(_sub[2].strftime("%Y-%m-%d"), '%Y-%m-%d').date()#创建日期
                result1wechat = self.connect.query(self.connect.fenqi, sql1wechat)  # 微信支付的消费结果
                result1deposit = self.connect.query(self.connect.fenqi, sql1deposit)  # 储值卡支付的消费结果
                money.extend(result1wechat)
                money.extend(result1deposit)
                del (result1wechat,result1deposit)
                if money:
                    for _,__ in money:
                        money_data.update({__.date(): money_data.get(__.date(), 0) + _})
                for i in range((end_date - start_date).days):# 统计每一天是否活跃
                    x = start_date + datetime.timedelta(i)#当前处在的天
                    y = x - datetime.timedelta(30)  # 在当天的前30天
                    count_money=0#当前天的前30天内的消费笔数
                    if x>cjrq:#当前日期大于创建日期才能有操作
                        if (x - cjrq).days >= 30:#上线满30天
                            if money_data:
                                for time in money_data:
                                    if time<=x and time>y:#消费时间在当前天的前30天之内
                                        count_money = count_money + 1#消费天数
                            if count_money>=16:
                                huoyue.update({_sub[1]: huoyue.get(_sub[1], 0) + 1})  # 门店活跃天数加1
                        elif (x - cjrq).days < 30: #上线不满30天
                            day=(x - cjrq).days//2+1
                            if money_data:
                                for time in money_data:
                                    if time<=x and time>=cjrq:
                                        count_money = count_money + 1#消费天数
                            if count_money>=day:
                                huoyue.update({_sub[1]: huoyue.get(_sub[1], 0) + 1})  # 门店活跃天数加1
        huoyue1 = sorted(huoyue.items(), key=lambda item: item[1], reverse=True)  # 按照次数排序
        huoyuename=[];huoyueday=[];count_=1
        totalamount = 0;# 得到总流水
        ls1=0#TOP10流水
        for name, amount in d1.items():
            totalamount = totalamount + amount
        for i in huoyue1:
            if i:
                if count_<10:
                    huoyuename.append(i[0])
                    huoyueday.append(i[1])
                    ls1=ls1+d1.get(i[0],0)
                    count_=count_+1
        if count_<10:
            for i in range(count_,11):
                huoyuename.append('_')
                huoyueday.append('_')
        zb1=round(ls1/totalamount,2)#流水占比
        huoyuename.append(zb1)#放到门店名称下面的一个格子里面
        all_data.append(huoyuename)
        all_data.append(huoyueday)

        #接上面第一个统计门店流水名称和流水
        ls2 = 0#TOP10门店流水
        d2 = sorted(d1.items(), key=lambda item: item[1], reverse=True)  # 按照流水金额排序得到top10流水
        dd1 = [];dd2 = [];count = 1
        for name,amount in d2:
            if name:
                if count < 10:
                    dd1.append(name)  # 门店名称
                    dd2.append(amount)  # 门店流水
                    ls2 = ls2 + d1.get(name, 0)#TOP10流水
                    count = count + 1
        if count < 10:
            for i in range(count, 11):
                dd1.append('-')
                dd2.append('-')
        zb2 = round(ls2 / totalamount, 2)  # 流水占比
        dd1.append(zb2)
        all_data.append(dd1)
        all_data.append(dd2)

        # 排序TOP10门店用券次数
        sql3deposit="""SELECT c.subbranch_name,-b.amount
                        FROM {0}.coupons_log a,{1}.user_deposit_card_log b,{1}.subbranch c
                        WHERE a.user_deposit_card_log_id=b.user_deposit_card_log_id and b.subbranch_id=c.subbranch_id
                        and a.create_time between '{2}' and '{3}'""".format(self.connect.coupons,self.connect.fenqi,
                                                                            start_date,end_date)
        sql3wechat="""SELECT c.subbranch_name,b.amount 
                        FROM {0}.coupons_log a,{1}.wechat_pay_log b,{1}.subbranch c
                        WHERE a.wechat_pay_log_id=b.wechat_pay_log_id and b.subbranch_id=c.subbranch_id
                        and a.create_time between '{2}' and '{3}'""".format(self.connect.coupons,self.connect.fenqi,
                                                                            start_date,end_date)
        result3deposit = self.connect.query('', sql3deposit)#微信用券日志
        result3wechat = self.connect.query('', sql3wechat)#储值卡用券日志
        data=[];data1={};data2={}
        data.extend(result3deposit)
        data.extend(result3wechat)
        del(result3deposit,result3wechat)
        for name,amount in data:
            data1.update({name: data1.get(name, 0) + amount})  # 金额
            data2.update({name: data2.get(name, 0) + 1})  # 用券次数
        data3 = sorted(data2.items(), key=lambda item: item[1], reverse=True)#按照次数排序
        d1_=[];d2_=[];d3_=[];count=1
        ls3=0
        for i in data3:
            if i:
                if count<10:
                    d1_.append(i[0])#门店名称
                    d2_.append(data2[i[0]])#门店用券次数
                    d3_.append(round(float(data1[i[0]]) / float(i[1]),2))#客单价
                    ls3= ls3 + d1.get(i[0], 0)#TOP10流水
                    count=count+1
        if count<10:
            for i in range(count,11):
                d1_.append('-')
                d2_.append('-')
                d3_.append('-')
        zb3=round(ls3 / totalamount, 2)  # 流水占比
        d1_.append(zb3)
        all_data.append(d1_)
        all_data.append(d2_)
        all_data.append(d3_)

        #TOP10TOP10客单价门店名称,在得到TOP10门店流水名称和流水已经得到了所有门店的流水d1,以及所有门店的消费笔数d1count
        kdj={}#用来存每个门店的名称和客单价
        for name in d1:
            if name:
                kdj.update({name: round(d1.get(name, 0) / d1count.get(name),2)})#保留两位小数
        kdj1=sorted(kdj.items(),key=lambda item:item[1],reverse=True)
        k1=[];k2=[];count=1
        ls4=0
        for i in kdj1:
            if i:
                if count<10:
                    k1.append(i[0])#门店名称
                    k2.append(i[1])#门店客单价
                    ls4 = ls4 + d1.get(i[0], 0)  # TOP10流水
                    count=count+1
        if count<10:
            for i in range(count,11):
                k1.append('-')
                k2.append('-')
        zb4 = round(ls4 / totalamount, 2)  # 流水占比
        k1.append(zb4)
        all_data.append(k1)
        all_data.append(k2)
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