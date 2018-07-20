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


    def shqxq(self, start_date, end_date, dir_name):
        enddate = datetime.datetime.strptime(start_date, '%Y-%m-%d').date() + datetime.timedelta(1)
        startdate = enddate - datetime.timedelta(14)
        columns = ['商户名','行政区', '微区域', '行业', '销售姓名', '运营姓名',
                   '最近15天({0}-{1})流水总额'.format(startdate,enddate), '最近15天({0}-{1})流水天数'.format(startdate,enddate)]
        all_data = []
        #直接找到所有商户（按照每个商户都有一个总店来去除多余的，并且微区域和行政区域都是总店的）
        sql1 = """SELECT b.merchant_id,a.subbranch_id,b.short_name,a.ADMIN_REGION_CODE,a.MICRO_REGION_CODE,
                    merchant_type_name,a.SALE_NAME, a.OPERATOR_NAME 
                    FROM subbranch a,merchant b, merchant_industry c 
                    WHERE a.merchant_id=b.merchant_id AND b.merchant_type = c.merchant_type and a.sub_type=1 and a.state=2"""
        sql1result = self.connect.query(self.connect.fenqi, sql1)
        for _sub in sql1result:
            dd1 = {}  # 用来存商户门下的所有门店的最近15天的总流水
            dd2 = {}  # 用来存商户门下的流水天数
            if _sub:
                _sub = list(_sub)#把一行有逗号的数据变成列表，把三四行政区code映射成name
                _sub[3] = self.connect.region_code2name(_sub[3]);#行政区
                _sub[4] = self.connect.region_code2name(_sub[4])#微区域
                data=[]
                data.extend([_sub[i] for i in range(2, 8)])#把result每一行的数据_sub放入_data列表中
                sql2 = """SELECT subbranch_id from subbranch WHERE merchant_id='{0}' and state=2 """.format(_sub[0])
                sql2result = self.connect.query(self.connect.fenqi, sql2)#得到每个商户的所有门店id，再来计算每家店的流水
                d1 = {}  # 用来存商户门下的所有门店的最近15天的流水
                d2 = {}  # 用来存所有每一天的金额数，主要是用来统计流水天数的
                for sub in sql2result:
                    if sub:
                        sql2wechat = """SELECT sum(amount),create_time FROM wechat_pay_log 
                                        WHERE subbranch_id='{0}' AND type IN (2,3) AND state=2 
                                        AND create_time between '{1}' and '{2}'
                                        GROUP BY create_time 
                                        ORDER BY create_time """.format(sub[0], startdate,enddate )#时间记得改成是最近15天
                        sql2deposit = """SELECT sum(-amount),create_time FROM user_deposit_card_log 
                                         WHERE subbranch_id='{0}' AND amount < 0 
                                         AND create_time between '{1}' and '{2}'
                                         GROUP BY create_time  
                                          ORDER BY create_time """.format(sub[0], startdate,enddate)
                        result2wechat = self.connect.query(self.connect.fenqi, sql2wechat)  # 遍历每个门店的微信流水
                        result2deposit = self.connect.query(self.connect.fenqi, sql2deposit)  # 遍历每个门店的储值卡流水
                        money2 = [];
                        money2.extend(result2deposit)
                        money2.extend(result2wechat)
                        del (result2deposit, result2wechat)
                        for i in money2:
                            if i:
                                d1.update({sub: d1.get(sub, 0) + i[0]})  # 所以d1存的是每个门店的id和总流水
                        for amount, time in money2:
                            if time:
                                d2.update({time.date(): d2.get(time.date(), 0) + amount})#所以门店遍历下来，保存他们的消费时间
                for md,ls in d1.items():
                    dd1.update({_sub[0]:dd1.get(_sub[0],0)+ls})
                len_date = len(set(d2.keys()))  # 时间长度，看有几天有流水
                dd2.update({_sub[0]:len_date})
                if dd1.get(_sub[0]):
                    data.extend([dd1.get(_sub[0]), dd2.get(_sub[0])])  # 增加商户近15天流水和天数
                else:
                    data.extend([0, dd2.get(_sub[0])])#增加商户近15天流水和天数
                bq_lq={}#装标签的name和领券数
                bq_yq={}#装标签的name和用券数
                sql3="""SELECT coupons_config_id from coupons_config
                        WHERE merchant_id='{0}'""".format(_sub[0])
                sql3result = self.connect.query(self.connect.coupons, sql3)#得到每一个门店的优惠券配置id
                for pzid in sql3result:
                    if pzid:
                        sql4="""SELECT label_id 
                                FROM coupons_cfg_label_rela
                                WHERE coupons_config_id='{0}'""".format(pzid[0])
                        sql4result = self.connect.query(self.connect.coupons, sql4)  # 得到每一个优惠券配置id对应的标签id
                        for bqid in sql4result:
                            if bqid:
                                sql5="""SELECT label_name FROM labels WHERE label_id='{0}'""".format(bqid[0])
                                sql5result = self.connect.query(self.connect.coupons, sql5)#得到该标签名称
                                sql6="""SELECT coupons_config_id 
                                        from coupons_cfg_label_rela
                                         WHERE label_id='{0}'""".format(bqid[0])
                                sql6result = self.connect.query(self.connect.coupons, sql6)  # 得到该标签对应多少个优惠券配置id
                                for i in sql6result:
                                    if i:
                                        sql7="""SELECT COUNT(*) FROM coupons
                                                        WHERE coupons_config_id='{0}'
                                                        AND create_time between '{1}' and '{2}'""".format(i[0],startdate,enddate)
                                        sql7result = self.connect.query(self.connect.coupons, sql7)#得到该配置id有多少张券被领了
                                        sql8="""SELECT COUNT(*) FROM coupons
                                                WHERE coupons_config_id='{0}' and `status`=1
                                                AND create_time between '{1}' and '{2}'""".format(i[0],startdate,enddate)
                                        sql8result = self.connect.query(self.connect.coupons, sql8)  # 得到该配置id有多少张券被用了
                                        bq_lq.update({sql5result[0][0]:sql7result[0][0]})
                                        bq_yq.update({sql5result[0][0]:sql8result[0][0]})
                countq=1
                for bq,lq in bq_lq.items():
                    if bq:
                        columns.append('券{0}标签'.format(countq))
                        columns.append('券{0}领券数/用券数'.format(countq))
                        data.append(bq)
                        d=str(lq)+'/'+str(bq_yq.get(bq))
                        data.append(d)
                        countq=countq+1
                all_data.append(data)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data, columns=columns)
        df.to_csv(os.path.join(dir_name, 'shqxq.csv'), index=False, encoding='gbk', sep=',')
        return all_data

def main():
    export = Export()
    #export.mdlszb('2018-6-1', '2018-6-3', r'\Users\qiqi\Desktop')
    export.shqxq('2018-7-18','2018-7-28', r'\Users\qiqi\Desktop')
    #export.mdpm('2018-1-03', '2018-7-30', r'\Users\qiqi\Desktop')
if __name__ == '__main__':
    main()