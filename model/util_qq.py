# encoding=utf-8
import MySQLdb
import datetime
import os
import pandas as pd
import connectTool
cwd = os.getcwd()
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

    def shqxq(self, start_date, end_date, dir_name, opt={}):
        enddate = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        startdate = enddate - datetime.timedelta(14)
        enddate1 = enddate + datetime.timedelta(1)
        columns = ['商户名','行政区', '微区域', '行业', '销售姓名', '运营姓名',
                   '最近15天({0}-{1})流水总额'.format(startdate,enddate), '最近15天({0}-{1})流水天数'.format(startdate,enddate)]
        all_data = []
        #直接找到所有商户（按照每个商户都有一个总店来去除多余的，并且微区域和行政区域都是总店的）
        sql1 = """SELECT b.merchant_id,a.subbranch_id,b.short_name,a.ADMIN_REGION_CODE,a.MICRO_REGION_CODE,
                    merchant_type_name,a.SALE_NAME, a.OPERATOR_NAME 
                    FROM subbranch a,merchant b, merchant_industry c 
                    WHERE a.merchant_id=b.merchant_id AND b.merchant_type = c.merchant_type and a.sub_type=1 and a.state=2"""
        if opt:
            _temp = ["{}='{}'".format(i,j) for i,j in opt.items() \
            if i not in ('MERCHANT_ID','MERCHANT_TYPE','SUBBRANCH_PROP')]
            _temp.extend(["b.{}='{}'".format(i,j) \
                for i,j in opt.items() if i in ('MERCHANT_ID','MERCHANT_TYPE')])
            sql1 += ' AND ' + ' AND '.join(_temp)
        sql1result = self.connect.query(self.connect.fenqi, sql1)

        labellist = []#用来放有多少标签的，便于补充‘-’
        for _sub in sql1result:
            dd1 = {}  # 用来存商户门下的所有门店的最近15天的总流水
            dd2 = {}  # 用来存商户门下的流水天数
            if _sub:
                _sub = list(_sub)#把一行有逗号的数据变成列表，把三四行政区code映射成name
                _sub[3] = self.connect.region_code2name(_sub[3]);#行政区
                _sub[4] = self.connect.region_code2name(_sub[4])#微区域
                data=[]
                for i in range(2,8):
                    if _sub[i]:
                        data.extend([_sub[i]])
                    else:
                        data.extend(['-'])
                #data.extend([_sub[i] for i in range(2, 8)])#把result每一行的数据_sub放入_data列表中
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
                                        ORDER BY create_time """.format(sub[0], startdate,enddate1 )#时间记得改成是最近15天
                        sql2deposit = """SELECT sum(-amount),create_time FROM user_deposit_card_log 
                                         WHERE subbranch_id='{0}' AND amount < 0 
                                         AND create_time between '{1}' and '{2}'
                                         GROUP BY create_time  
                                          ORDER BY create_time """.format(sub[0], startdate,enddate1)
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

                #每一个商户
                bq_lq={}#装标签的name和领券数
                bq_yq={}#装标签的name和用券数
                bq=[]#所有的标签id集合
                sql3="""SELECT coupons_config_id from coupons_config
                        WHERE merchant_id='{0}'""".format(_sub[0])
                sql3result = self.connect.query(self.connect.coupons, sql3)#得到每一个商户的优惠券配置id
                for pzid in sql3result:
                    #print(pzid)
                    if pzid:
                        sql4="""SELECT label_id 
                                FROM coupons_cfg_label_rela
                                WHERE coupons_config_id='{0}'""".format(pzid[0])
                        sql4result = self.connect.query(self.connect.coupons, sql4)  # 得到每一个优惠券配置id对应的标签id
                        #print(sql4result)
                        bq.extend([i[0] for i in sql4result]) #每一个优惠券对应的标签都放进去
                #print(bq)
                #print(set(bq))
                #相等于遍历一个商户的所有标签id
                for bqid in set(bq):
                    if bqid:
                        lq_count = 0  # 记录领券和用券总数
                        yq_count = 0
                        #print(bqid)
                        sql5 = """SELECT label_name FROM labels WHERE label_id='{0}'""".format(bqid)
                        sql5result = self.connect.query(self.connect.coupons, sql5)  # 得到该标签名称
                        #print(sql5result)
                        sql6 = """SELECT coupons_config_id from coupons_cfg_label_rela
                                  WHERE label_id='{0}'""".format(bqid)
                        sql6result = self.connect.query(self.connect.coupons, sql6)  # 得到该标签对应多少个优惠券配置id
                        #print('coupons_config_id:{0}'.format(sql6result))
                        for i in sql6result:
                            if i:
                                sql6_6 = """select merchant_id from coupons_config 
                                WHERE coupons_config_id='{0}'""".format(i[0])
                                sql6_6result = self.connect.query(self.connect.coupons, sql6_6)  # 返回该优惠券配置id属于哪个商户
                                #print("d")
                                #print(sql6_6result)
                                if sql6_6result[0][0] == _sub[0]:  # 如果为本循环下的商户，则计算该标签所对应的配置id对应的优惠券的领券数和用券数目
                                    #print(i[0])
                                    #print("t")
                                    sql7 = """SELECT COUNT(*) FROM coupons WHERE 
                                    coupons_config_id='{0}' AND create_time between '{1}' and 
                                    '{2}'""".format(i[0], start_date, end_date)
                                    sql7result = self.connect.query(self.connect.coupons, sql7)  # 得到该配置id有多少张券被领了
                                    sql8 = """SELECT COUNT(*) FROM coupons WHERE coupons_config_id='{0}' and `status`=1
                                              AND create_time between '{1}' and '{2}'""".format(i[0], start_date, end_date)
                                    sql8result = self.connect.query(self.connect.coupons, sql8)  # 得到该配置id有多少张券被用了
                                    #print("the re7 is {0},and the re8 is {1}".format(sql7result[0][0], sql8result[0][0]))
                                    lq_count = lq_count + sql7result[0][0]
                                    yq_count = yq_count + sql8result[0][0]
                        #print("the re77 is {0},and the re88 is {1}".format(lq_count, yq_count))
                        bq_lq.update({sql5result[0][0]: lq_count})
                        bq_yq.update({sql5result[0][0]: yq_count})

                countq=1
                for bq,lq in bq_lq.items():
                    if bq:
                        label1='券{0}标签'.format(countq)
                        label2='券{0}领券数\用券数'.format(countq)
                        if label1 not in columns:
                            columns.append('券{0}标签'.format(countq))
                            labellist.append('券{0}标签'.format(countq))
                        if label2 not in columns:
                            columns.append('券{0}领券数\用券数'.format(countq))
                            labellist.append('券{0}领券数\用券数'.format(countq))
                        data.append(bq)
                        d=str(lq)+'\\'+str(bq_yq.get(bq))
                        data.append(d)
                        #print("商户是：{2},标签是：{0}，领券数是：{1}".format(bq,d,_sub[2]))
                        countq=countq+1
                #print(data)
            all_data.append(data)

        # if not os.path.exists(dir_name):
        #     os.makedirs(dir_name)
        # df = pd.DataFrame(all_data, columns=columns)
        # for i in labellist:
        #     if i:
        #         df[i] = df[i].fillna('-')
        # df.to_csv(os.path.join(dir_name, 'shqxq.csv'), index=False, encoding='gbk', sep=',')

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data, columns=columns)
        for i in labellist:
            if i:
                df[i] = df[i].fillna('-')
        return df,'商户券详情'


    def mdpm(self, start_date, end_date, dir_name,opt={}):
        indexs = []
        indexs.extend(['排名', '活跃门店名称', '活跃门店活跃天数', '流水门店名称', '流水门店流水'
                      , '用券次数门店名称','用券次数门店总用券次数', '用券次数门店客单价',
                       '客单价门店名称', '客单价门店客单价'])
        all_data = []
        top = ['TOP1', 'TOP2', 'TOP3', 'TOP4', 'TOP5', 'TOP6', 'TOP7', 'TOP8', 'TOP9', 'TOP10', 'TOP10门店流水总比重']
        all_data.append(top)
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        #end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()+ datetime.timedelta(1)
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
                d2.update({_sub[1]:d2.get(_sub[1],0)+len_date})
        # 计算门店总流水
        totalamount=0
        for name,money in d1.items():
                totalamount=totalamount+money
        #统计TOP10活跃门店名称
        dd2 = sorted(d2.items(), key=lambda item: item[1], reverse=True)  # 按照活跃天数排序得到top10活跃天数
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
                hylie2.append('0')
        if totalamount:
            hyzb = round(hytopls / totalamount, 3)  # 流水占比
        else:
            hyzb = 0
        hyzb=hyzb*100
        hylie1.append(str(hyzb)+'%')
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
                lslie2.append('0')
        if totalamount:
            lszb = round(lstopls / totalamount, 3)  # 流水占比
        else:
            lszb=0
        lszb=lszb*100
        lslie1.append(str(lszb)+'%')
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
        data3 = sorted(data2.items(), key=lambda item: item[1], reverse=True)  # 门店和用券次数,按照次数排序
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
                yqlie2.append('0')
                yqlie3.append('0')
        if totalamount:
            zb3 = round(yqtopls / totalamount, 3)  # 流水占比
        else:
            zb3=0
        zb3=zb3*100
        yqlie1.append(str(zb3)+'%')
        all_data.append(yqlie1)
        all_data.append(yqlie2)
        all_data.append(yqlie3)

        #TOP10客单价门店名称
        kdj = {}  # 用来存每个门店的名称和客单价
        for name,amount in d1.items():
            if amount:
                kdj.update({name: round(d1.get(name, 0) / d1count.get(name), 3)})  # 保留两位小数
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
                kdjlie2.append('0')
        if totalamount:
            zb4 = round(kdjtopls / totalamount, 3)  # 流水占比
        else:
            zb4=0
        zb4=zb4*100
        kdjlie1.append(str(zb4)+'%')
        all_data.append(kdjlie1)
        all_data.append(kdjlie2)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data,index=indexs)
        df = df.stack().unstack(0)
        return df, '门店排名'

        # if not os.path.exists(dir_name):
        #     os.makedirs(dir_name)
        # df = pd.DataFrame(all_data, index=indexs)
        # df = df.stack().unstack(0)
        # df.to_csv(os.path.join(dir_name, 'mdpm.csv'), index=False, encoding='gbk', sep=',')


def main():
    export = Export()
    opt = {
        'ADMIN_REGION_CODE':'2100'
        #'SUBBRANCH_ID': '00yfmeirongzhengjiadian90m8op'
        #'MERCHANT_ID': 'ed3325d31cea4333b62b76eafeb426e5'
    }
    #export.mdlszb('2018-6-1', '2018-6-3', r'\Users\qiqi\Desktop')
    #export.shqxq('2017-5-18','2018-8-28', r'\Users\16538\Desktop', opt)
    export.shqxq('2018-5-1', '2018-5-3', r'\Users\qiqi\Desktop', opt)
    #export.mdpm('2018-8-5', '2018-9-5', r'\Users\16538\Desktop')

if __name__ == '__main__':
    main()