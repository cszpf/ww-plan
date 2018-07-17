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
    
    # 将行政区code映射成name
    def region_code2name(self,code):
        sql = "SELECT region_name FROM micro_region WHERE region_code='{code}'".format(code=code)
        result = self.query(self.fenqi,sql)
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
        WHERE a.merchant_id=b.merchant_id AND b.merchant_type = c.merchant_type AND a.create_time!='' """
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
                ddtgrq = _sub[-1].date() if _sub[-1] != '' else datetime.date(2017,1,1)#到店推广日期
                if data:#有消费记录
                    # 每一天门店流水
                    for _,__ in data:#消费金额和消费时间
                        data1.update({__.date():data1.get(__.date(),0)+_})
                    del(data)
                    max_date = max(data1.keys())
                    len_date = len([_ for _ in data1.keys() if (end_date - _).days<=30])
                    ifactive = True if len_date >= (16 if (end_date-ddtgrq).days >= 30 else (end_date-ddtgrq).days//2 + 1) else False
                    ifsilent = True if (end_date - max_date).days >= 15 else False
                else:#没有消费记录
                    ifactive = False; ifsilent = True if (end_date - ddtgrq).days >= 15 else False
                _data.extend([ifactive, ifsilent])
                for i in range((end_date-start_date).days):
                    x = start_date + datetime.timedelta(i)
                    _data.append(data1.get(x,0))
            all_data.append(_data)
        # print(all_data)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data,columns=columns)
        df.to_csv(os.path.join(dir_name,'mdls.csv'),index=False,encoding='gbk',sep=',')
        return all_data

        # 实现门店流水占比表的在线生成
    def mdlszb(self, start_date, end_date, dir_name):
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
        merchant_type_name,SALE_NAME, OPERATOR_NAME,a.create_time,AVERAGE_ASSESS_INCOME 
        FROM subbranch a,merchant b, merchant_industry c 
        WHERE a.merchant_id=b.merchant_id AND b.merchant_type = c.merchant_type AND a.create_time!='' """
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
                ddtgrq = _sub[8].date()#到店推广日期
                if data:#有消费记录
                    # 每一天门店流水
                    for _,__ in data:#消费金额和消费时间
                        data1.update({__.date():data1.get(__.date(),0)+_})
                    del(data)
                    max_date = max(data1.keys())
                    len_date = len([_ for _ in data1.keys() if (end_date - _).days<=30])
                    ifactive = True if len_date >= (16 if (end_date-ddtgrq).days >= 30 else (end_date-ddtgrq).days//2 + 1) else False
                    ifsilent = True if (end_date - max_date).days >= 15 else False
                else:#没有消费记录
                    ifactive = False; ifsilent = True if (end_date - ddtgrq).days >= 15 else False
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

def main():
    export = Export()
    export.mdlszb('2018-6-1','2018-6-3','./')

if __name__ == '__main__':
    main()