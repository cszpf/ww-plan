#encoding=utf-8
from flask import jsonify
import MySQLdb
import datetime
import os
import pandas as pd
import util_yj as yj
import util_lz as lz
import util_lcs as lcs
import util_qq as qq
import connectTool
import myclick as click
cwd = os.getcwd()
def concat(df, n):
    '''
    df:需要汇总统计的表<pd.DataFrame>
    n:非日期列数<int>
    return:汇总之后的表<pd.DataFrame>
    '''
    x = pd.DataFrame(columns=df.columns)
    temp = ['汇总']
    temp.extend(['-' for i in range(n-1)])
    x[df.columns[n:]] = pd.DataFrame(df[df.columns[n:]].sum()).T
    x[df.columns[:n]] = temp
    return pd.concat([df, x], ignore_index=True)

class Connect(connectTool.connect):
    
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
    def mdls(self, start_date, end_date, dir_name, opt={}):
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
        WHERE a.merchant_id=b.merchant_id AND b.merchant_type = c.merchant_type AND a.create_time IS NOT NULL """
        if opt:
            _temp = ["{}='{}'".format(i,j) for i,j in opt.items() \
            if i not in ('MERCHANT_ID','MERCHANT_TYPE','SUBBRANCH_PROP')]
            _temp.extend(["b.{}='{}'".format(i,j) \
                for i,j in opt.items() if i in ('MERCHANT_ID','MERCHANT_TYPE')])
            sql1 += ' AND ' + ' AND '.join(_temp)
        result = self.connect.query(self.connect.fenqi, sql1)
        for _sub in result:
            if _sub:
                data = []; data1 = {}; _data = []; _sub=list(_sub)
                _sub[3] = self.connect.region_code2name(_sub[3])
                _sub[4] = self.connect.region_code2name(_sub[4])
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
                    len_date = len([_ for _ in data1.keys() if (end_date - _).days<=30 and (end_date - _).days>0])
                    ifactive = True if len_date >= (16 if (end_date-ddtgrq).days >= 30 else (end_date-ddtgrq).days//2 + 1) else False
                    ifsilent = True if (end_date - max_date).days >= 15 else False
                else:#没有消费记录
                    ifactive = False; ifsilent = True if (end_date - ddtgrq).days >= 15 else False
                _data.extend([ifactive, ifsilent])
                if 'SUBBRANCH_PROP' in opt.keys():
                    if (opt['SUBBRANCH_PROP'] == 'active' and not ifactive) or (opt['SUBBRANCH_PROP'] == 'silent' and not ifsilent):
                        continue
                for i in range((end_date-start_date).days):
                    x = start_date + datetime.timedelta(i)
                    _data.append(data1.get(x,0))
            all_data.append(_data)
        df = pd.DataFrame(all_data,columns=columns)
        df = concat(df, 10)
        return df, '门店流水'

    # 实现门店流水占比表的在线生成
    def mdlszb(self, start_date, end_date, dir_name, opt={}):
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
        WHERE a.merchant_id=b.merchant_id AND b.merchant_type = c.merchant_type AND a.create_time IS NOT NULL """
        if opt:
            _temp = ["{}='{}'".format(i,j) for i,j in opt.items() \
            if i not in ('MERCHANT_ID','MERCHANT_TYPE','SUBBRANCH_PROP')]
            _temp.extend(["b.{}='{}'".format(i,j) \
                for i,j in opt.items() if i in ('MERCHANT_ID','MERCHANT_TYPE')])
            sql1 += ' AND ' + ' AND '.join(_temp)
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
                    len_date = len([_ for _ in data1.keys() if (end_date - _).days<=30 and (end_date - _).days>0])
                    # print(len_date)
                    ifactive = True if len_date >= (16 if (end_date-ddtgrq).days >= 30 else (end_date-ddtgrq).days//2 + 1) else False
                    ifsilent = True if (end_date - max_date).days >= 15 else False
                else:#没有消费记录
                    ifactive = False; ifsilent = True if (end_date - ddtgrq).days >= 15 else False
                _data.extend([ifactive, ifsilent])
                if 'SUBBRANCH_PROP' in opt.keys():
                    if (opt['SUBBRANCH_PROP'] == 'active' and not ifactive) or (opt['SUBBRANCH_PROP'] == 'silent' and not ifsilent):
                        continue
                for i in range((end_date-start_date).days):
                    x = start_date + datetime.timedelta(i)
                    try:
                        _zb = round(float(data1.get(x,0))/float(_sub[-1]),3)
                    except:
                        _zb = 0
                    finally:
                        _data.append(_zb)
            all_data.append(_data)
        df = pd.DataFrame(all_data,columns=columns)
        df = concat(df, 10)
        return df, '门店流水占比'
    
    def shyq(self, start_date, end_date, dir_name, opt={}):
        yj_Export = yj.Export()
        _df, _name = yj_Export.shyq(start_date, end_date, dir_name)
        return _df, _name

    def qpm(self, start_date, end_date, dir_name, opt={}):
        yj_Export = yj.Export()
        return yj_Export.qpm(start_date, end_date, dir_name)

    def mdhz(self, start_date, end_date, dir_name, opt={}):
        lz_EXport = lz.Export()
        return lz_EXport.mdhz(start_date, end_date, dir_name)

    def khhz(self, start_date, end_date, dir_name, opt={}):
        lcs_export = lcs.Export()
        return lcs_export.khhz(start_date, end_date, dir_name)
    
    def qhz(self, start_date, end_date, dir_name, opt={}):
        lcs_export = lcs.Export()
        yj_export = yj.Export()
        df, names = [], []
        qhz = lcs_export.qhz(start_date, end_date, dir_name)
        df.append(qhz[0]); names.append(qhz[1])
        ydqxq = yj_export.ydqxq(start_date, end_date, dir_name)
        df.extend(ydqxq[0]); names.extend(ydqxq[1])
        return df, names

    def mdpm(self, start_date, end_date, dir_name, opt={}):
        qq_export = qq.Export()
        return qq_export.mdpm(start_date, end_date, dir_name)

    def shqxq(self, start_date, end_date, dir_name, opt={}):
        qq_export = qq.Export()
        return qq_export.shqxq(start_date,end_date,dir_name)

    def djl(self, start_date, end_date, dir_name, opt={}):
        path = '../static/click'
        if not os.path.exists(path):
            path = './static/click'
        df1 = pd.read_csv(os.path.join(path,'click.csv'), encoding='gbk')
        last_day = datetime.datetime.strptime(df1.columns[-1],'%Y-%m-%d')
        end_day = datetime.datetime.strptime(end_date,'%Y-%m-%d')
        if (end_day - last_day).days > 1:
            df2 = click.preDate(df1.columns[-1], end_date)
            df1 = pd.merge(df1.drop(df1.columns[-1], axis=1), df2, on='受访页面', how='outer', copy=False).fillna(0)
            # os.remove(os.path.join(path, 'click.csv'))
            click.write_csv(df1, path)
        option = ['受访页面']
        option.extend(df1.columns[1:][[i<=end_date and i>=start_date for i in df1.columns[1:]]])
        return df1[option], '点击量'

def main():
    export = Export()
    # opt = {
    # 'SUBBRANCH_ID':'91dc20c9adac4035a4c1b7964792b043',
    # 'SUBBRANCH_PROP':'active'
    # }
    # print(export.mdls('2018-6-1','2018-6-3','./', {})[0].to_dict())
    export.shyq('2018-6-1','2018-6-3','./')
    # print(jsonify(export.mdlszb('2018-6-1','2018-6-3','./', {})[0].to_json()))

if __name__ == '__main__':
    main()