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
        self.ip2, self.user2, self.pwd2, self.port2 = '192.168.1.30', 'root', 'Wangwang@scut123', 3306
    
    # 数据库连接
    def connect(self, db_name, _id='1'):
        # _id:'1'表示大学城数据库,'2'表示汪汪数据库
        if(db_name != ''):
            db = eval("""MySQLdb.connect(self.ip{id}, self.user{id}, self.pwd{id}, 
            db_name, port=self.port{id}, charset='utf8')""".format(id=_id))
        else:   #需要跨数据库（fenqi、coupons）查询时则不指定数据库
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
    def region_code2name(self,code):
        sql = "SELECT region_name FROM micro_region WHERE region_code='{code}'".format(code=code)
        result = self.query(self.fenqi,sql)
        if result:
            return result[0][0]
        return None

class Export:
    def __init__(self):
        self.connect = Connect()

    def shyq(self, start_date, end_date, dir_name):
        columns = ['商户','行政区', '微区域', '行业', '销售姓名', '运营姓名', '流水', '消费笔数', '客单价', '关注券领券数',
                   '关注券用券数', '关注券数量', '关注券客单价', '关注券使用率', '促活券领券数', '促活券用券数', '促活券数量',
                   '促活券客单价', '促活券使用率', '邻店券领券数', '邻店券客单价', '邻店券用券数', '帮邻店发券数',
                   '帮邻店发券后的使用数', '回头客', '办卡数', '办卡金额']
        all_data = []
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # 取商户对应的总店的行政区、微区域、行业、销售姓名、运营姓名
        sql0 = '''select merchant.merchant_id, admin_region_code, micro_region_code, merchant_type_name, sale_name, operator_name 
        from subbranch, merchant, merchant_industry where subbranch.merchant_id=merchant.merchant_id and 
        merchant.merchant_type=merchant_industry.merchant_type and sub_type=1 '''
        result0 = self.connect.query(self.connect.fenqi, sql0)
        res0 = {}
        for mer in result0:
            res0[mer[0]]=[self.connect.region_code2name(mer[1]) if mer[1]!=None and mer[1]!=''else '-',
                         self.connect.region_code2name(mer[2]) if mer[2]!=None and mer[2]!=''else '-',
                         mer[3], mer[4] if mer[4]!=None and mer[4]!=''else '-', mer[5]if mer[5]!=None and mer[5]!=''else '-']

        # 计算商户流水、消费笔数、客单价、办卡数、办卡金额
        sql_wechat = '''(select merchant_id, sum(amount)as sum1, count(*)as num1 from merchant, wechat_pay_log as wpl, user
        where merchant.merchant_config_id = user.merchant_config_id and user.user_id = wpl.user_id and wpl.state = 2 
        and wpl.type in (2,3) and wpl.create_time > '{}' and wpl.create_time < '{}' group by merchant_id)
        as pay1'''.format(start_date, end_date)
        sql_dc = '''(select merchant_id, sum(abs(amount))as sum2, count(*)as num2 from user_deposit_card as dc, 
        user_deposit_card_log as dcl where dc.user_deposit_card_id = dcl.user_deposit_card_id and amount < 0 and 
        dcl.create_time > '{}' and dcl.create_time < '{}' group by merchant_id)as pay2'''.format(start_date, end_date)
        sql_recharge = '''(select merchant_id, sum(amount)as recharge_total, count(*)as recharge_num from user_deposit_card as dc, 
        user_deposit_card_log as dcl where dc.user_deposit_card_id = dcl.user_deposit_card_id and amount > 0 and 
        dcl.create_time > '{}' and dcl.create_time < '{}' group by merchant_id)as recharge'''.format(start_date, end_date)
        sql_mer = '''(select merchant.merchant_id,merchant.short_name from subbranch, merchant 
        where subbranch.merchant_id=merchant.merchant_id and sub_type=1)as merList'''
        sql1 = '''select merList.merchant_id, short_name, (ifnull(sum1,0)+ifnull(sum2,0))as amount,(ifnull(num1,0)+ifnull(num2,0))as num,  
        ifnull(recharge_num,0), ifnull(recharge_total,0) from {} left join {} on merList.merchant_id=pay1.merchant_id left join {} on merList.merchant_id=
        pay2.merchant_id left join {} on merList.merchant_id=recharge.merchant_id'''.format(sql_mer, sql_wechat, sql_dc, sql_recharge)
        result1 = self.connect.query(self.connect.fenqi, sql1)
        mer = []    #mer是merchant_id的list
        res1 = {}
        for _mer in result1:
            mer.append(_mer[0])
            res1[_mer[0]] = [_mer[1],_mer[2],_mer[3],_mer[2]/_mer[3] if _mer[3]!=0 else 0, _mer[4], _mer[5]]
            #res1词典的key为merchant_id, value为 列表[商户简称、商户流水、消费笔数、客单价、办卡数、办卡金额]

        # 关注券、促活券、邻店券统计
        GZ = '145556';CH = '145558'
        sql_merList = '''select merchant_id from {}.merchant'''
        sql_coupons = '''select merchant_id, count(*)as num from coupons, coupons_cfg_label_rela as cl, coupons_config 
        where coupons.coupons_config_id=cl.coupons_config_id and coupons.coupons_config_id=coupons_config.coupons_config_id 
        and label_id = '{}' and coupons.create_time > '{}' and coupons.create_time < '{}' {} group by merchant_id;'''
        sql_launch = '''select merchant_id, count(*) from coupons_config, coupons_cfg_label_rela as cl where 
                coupons_config.coupons_config_id=cl.coupons_config_id and label_id='{}' and coupons_config.status=2 group by merchant_id;'''
        sql_GZ_get = sql_coupons.format(GZ, start_date, end_date, '')
        sql_GZ_use = sql_coupons.format(GZ, start_date, end_date, 'and coupons.status=1')
        sql_GZ_launch = sql_launch.format(GZ)
        sql_CH_get = sql_coupons.format(CH, start_date, end_date, '')
        sql_CH_use = sql_coupons.format(CH, start_date, end_date, 'and coupons.status=1')
        sql_CH_launch = sql_launch.format(CH)

        sql_cou_wechat = '''select cc.merchant_id, sum(wl.amount)as sum1, count(*)as num1 from {coupons}.coupons_log as cl, {fenqi}.wechat_pay_log as wl,
        {coupons}.coupons as c, {coupons}.coupons_cfg_label_rela as l, {coupons}.coupons_config as cc where cl.wechat_pay_log_id=wl.wechat_pay_log_id and 
        cl.coupons_id=c.coupons_id and c.coupons_config_id=l.coupons_config_id and c.coupons_config_id=cc.coupons_config_id and wl.state=2 and wl.type=3 and 
        l.label_id='{label_id}' and wl.create_time>'{start_time}' and wl.create_time<'{end_time}' group by cc.merchant_id'''
        sql_cou_dc = '''select cc.merchant_id, sum(abs(dl.amount))as sum2,count(*)as num2 from {coupons}.coupons_log as cl, {fenqi}.user_deposit_card_log as dl,
        {coupons}.coupons as c, {coupons}.coupons_cfg_label_rela as l, {coupons}.coupons_config as cc 
        where cl.user_deposit_card_log_id=dl.user_deposit_card_log_id and cl.coupons_id=c.coupons_id and c.coupons_config_id=l.coupons_config_id 
        and c.coupons_config_id=cc.coupons_config_id and dl.amount<0 and l.label_id='{label_id}' and dl.create_time>'{start_time}' and dl.create_time<'{end_time}' group by cc.merchant_id'''
        sql_avg = '''select merList.merchant_id, if((ifnull(num1,0)+ifnull(num2,0))=0,0,(ifnull(sum1,0)+ifnull(sum2,0))/(ifnull(num1,0)+ifnull(num2,0)))
        as avg_amount from ({})as merList left join ({})as cw on merList.merchant_id=cw.merchant_id left join ({})as cd 
        on merList.merchant_id=cd.merchant_id'''
        sql_GZ_avg = sql_avg.format(sql_merList.format(self.connect.fenqi), sql_cou_wechat.format(coupons=self.connect.coupons, fenqi=self.connect.fenqi,
        label_id=GZ, start_time=start_date, end_time=end_date), sql_cou_dc.format(coupons=self.connect.coupons, fenqi=self.connect.fenqi,
        label_id=GZ, start_time=start_date, end_time=end_date))
        sql_CH_avg = sql_avg.format(sql_merList.format(self.connect.fenqi), sql_cou_wechat.format(coupons=self.connect.coupons, fenqi=self.connect.fenqi,
        label_id=CH, start_time=start_date, end_time=end_date), sql_cou_dc.format(coupons=self.connect.coupons, fenqi=self.connect.fenqi,
        label_id=CH, start_time=start_date, end_time=end_date))

        #邻店帮我
        LD_help = '''select merchant_id,count(*)as num from coupons, coupons_config where 
        coupons.coupons_config_id=coupons_config.coupons_config_id and coupons.{time}>'{start_time}' 
        and coupons.{time}<'{end_time}' and coupons.coupons_promote_id is not null group by merchant_id'''
        LD_help_get = LD_help.format(time='create_time', start_time=start_date, end_time=end_date)
        LD_help_use = LD_help.format(time='used_time', start_time=start_date, end_time=end_date)
        LD_help_wechat = '''select cc.merchant_id, count(*)as num1, sum(wl.amount)as sum1 from {coupons}.coupons c, 
        {coupons}.coupons_config cc, {coupons}.coupons_log cl, {fenqi}.wechat_pay_log wl
        where c.coupons_id=cl.coupons_id and cl.wechat_pay_log_id=wl.wechat_pay_log_id and c.coupons_config_id=cc.coupons_config_id
        and c.used_time>'{start_time}' and c.used_time<'{end_time}' and wl.state=2 and wl.type=3
        and c.coupons_promote_id is not null group by merchant_id'''.format(coupons=self.connect.coupons, fenqi=self.connect.fenqi,
        start_time=start_date, end_time=end_date)
        LD_help_dc = '''select cc.merchant_id, count(*)as num2, sum(abs(dl.amount))as sum2 from {coupons}.coupons c, 
        {coupons}.coupons_log cl, {coupons}.coupons_config cc, {fenqi}.user_deposit_card_log dl
        where c.coupons_id=cl.coupons_id and cl.user_deposit_card_log_id=dl.user_deposit_card_log_id
        and c.coupons_config_id=cc.coupons_config_id and c.used_time>'{start_time}' and c.used_time<'{end_time}' and dl.amount<0 
        and c.coupons_promote_id is not null group by merchant_id'''.format(coupons=self.connect.coupons, fenqi=self.connect.fenqi,
        start_time=start_date, end_time=end_date)
        LD_help_avg = '''select merList.merchant_id,if((ifnull(num1,0)+ifnull(num2,0))=0,0,(ifnull(sum1,0)+ifnull(sum2,0))/(ifnull(num1,0)+ifnull(num2,0)))
        as avg_amount from ({})as merList left join ({})as lw on merList.merchant_id=lw.merchant_id left join ({})as ld
        on merList.merchant_id=ld.merchant_id'''.format(sql_merList.format(self.connect.fenqi), LD_help_wechat, LD_help_dc)
        #我帮邻店
        help_LD = '''select merchant_id,count(*)as num from coupons, coupons_promote where 
        coupons.coupons_promote_id=coupons_promote.coupons_promote_id and coupons.{time}>'{start_time}' 
        and coupons.{time}<'{end_time}' group by merchant_id'''
        help_LD_get = help_LD.format(time='create_time', start_time=start_date, end_time=end_date)
        help_LD_use = help_LD.format(time='used_time', start_time=start_date, end_time=end_date)

        result2 = [self.connect.query(self.connect.coupons, sql_GZ_get), self.connect.query(self.connect.coupons, sql_GZ_use),
                   self.connect.query(self.connect.coupons, sql_GZ_launch), self.connect.query('',sql_GZ_avg),
                   self.connect.query(self.connect.coupons, sql_CH_get), self.connect.query(self.connect.coupons, sql_CH_use),
                   self.connect.query(self.connect.coupons, sql_CH_launch), self.connect.query('',sql_CH_avg),
                   self.connect.query(self.connect.coupons, LD_help_get), self.connect.query('', LD_help_avg),
                   self.connect.query(self.connect.coupons, LD_help_use), self.connect.query(self.connect.coupons, help_LD_get),
                   self.connect.query(self.connect.coupons, help_LD_use)]
        res2 = {}
        for i in range(len(result2)):
            if len(result2[i]) > 0:
                for _mer in result2[i]:
                    if _mer[0] not in res2:
                        res2[_mer[0]] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    res2[_mer[0]][i] = _mer[1]

        #回头客
        sql_wechat = '''(select user_id, count(*)as num1 from wechat_pay_log where state = 2 and type in (2,3) 
        and create_time > '{}' and create_time < '{}' group by user_id)as userw'''.format(start_date, end_date)
        sql_dc = '''(select user_id, count(*)as num2 from user_deposit_card as dc, user_deposit_card_log as dcl 
        where dc.user_deposit_card_id=dcl.user_deposit_card_id and amount<0 and dcl.create_time > '{}' and 
        dcl.create_time < '{}' group by user_id)as userd'''.format(start_date, end_date)
        sql_userList = '''(select user_id, merchant_id from user, merchant where user.merchant_config_id=
        merchant.merchant_config_id)as userList'''
        sql = '''select merchant_id, count(*) from {} left join {} on userList.user_id = userw.user_id left join {} 
        on userList.user_id = userd.user_id where ifnull(userw.num1,0)+ifnull(userd.num2,0)>1 group by 
        userList.merchant_id'''.format(sql_userList, sql_wechat, sql_dc)
        result3 = self.connect.query(self.connect.fenqi, sql)
        res3 = {}    #res是商户id映射到回头客数的词典
        for _mer in result3:
            res3[_mer[0]] = _mer[1]

        for mID in mer:
            _data = []
            _data.append(res1[mID][0])
            _data.extend(res0[mID][0:5] if mID in res0 else ['-','-','-','-','-'])
            _data.extend(res1[mID][1:4])
            _data.extend(res2[mID][0:4])
            _data.append(res2[mID][1]/res2[mID][0] if res2[mID][0]>0 else 0)
            _data.extend(res2[mID][4:8])
            _data.append(res2[mID][5]/res2[mID][4] if res2[mID][4]>0 else 0)
            _data.extend(res2[mID][8:13])
            _data.append(res3.get(mID, 0))
            _data.extend(res1[mID][4:6])
            all_data.append(_data)
        # print(all_data)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data,columns=columns)
        df.to_csv(os.path.join(dir_name,'shyq.csv'),index=False,encoding='gbk',sep=',')
        return all_data

def main():
    export = Export()
    # export.mdls('2018-6-1','2018-6-3','./')
    export.shyq('2017-6-1','2018-7-16','./')

if __name__ == '__main__':
    main()