import MySQLdb
import datetime
import os
import pandas as pd
from decimal import Decimal
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

    # 生成行政区、微区域code映射成name的表（字典）
    def region_code2name(self):
        sql = '''select region_code, region_name from micro_region'''
        result = self.query(self.fenqi, sql)
        dict = {}
        for pair in result:
            dict[pair[0]] = pair[1]
        return dict

    # 查询对应标签的券的客单价的sql语句
    def coupons_avg(self, label_id, start_date, end_date):
        sql_merList = '''select merchant_id from {}.merchant'''
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
        return sql_avg.format(sql_merList.format(self.fenqi),
                              sql_cou_wechat.format(coupons=self.coupons, fenqi=self.fenqi, label_id=label_id, start_time=start_date, end_time=end_date),
                              sql_cou_dc.format(coupons=self.coupons, fenqi=self.fenqi, label_id=label_id, start_time=start_date, end_time=end_date))

    # 查询邻店券的客单价的sql语句
    def getSQL_LD_avg(self, start_date, end_date):
        sql_merList = '''select merchant_id from {}.merchant'''
        LD_help_wechat = '''select cc.merchant_id, count(*)as num1, sum(wl.amount)as sum1 from {coupons}.coupons c, 
        {coupons}.coupons_config cc, {coupons}.coupons_log cl, {fenqi}.wechat_pay_log wl
        where c.coupons_id=cl.coupons_id and cl.wechat_pay_log_id=wl.wechat_pay_log_id and c.coupons_config_id=cc.coupons_config_id
        and c.used_time>'{start_time}' and c.used_time<'{end_time}' and wl.state=2 and wl.type=3
        and c.coupons_promote_id is not null group by merchant_id'''.format(coupons=self.coupons, fenqi=self.fenqi,
        start_time=start_date, end_time=end_date)
        LD_help_dc = '''select cc.merchant_id, count(*)as num2, sum(abs(dl.amount))as sum2 from {coupons}.coupons c, 
        {coupons}.coupons_log cl, {coupons}.coupons_config cc, {fenqi}.user_deposit_card_log dl
        where c.coupons_id=cl.coupons_id and cl.user_deposit_card_log_id=dl.user_deposit_card_log_id
        and c.coupons_config_id=cc.coupons_config_id and c.used_time>'{start_time}' and c.used_time<'{end_time}' and dl.amount<0 
        and c.coupons_promote_id is not null group by merchant_id'''.format(coupons=self.coupons, fenqi=self.fenqi,
        start_time=start_date, end_time=end_date)
        LD_help_avg = '''select merList.merchant_id,if((ifnull(num1,0)+ifnull(num2,0))=0,0,(ifnull(sum1,0)+ifnull(sum2,0))/(ifnull(num1,0)+ifnull(num2,0)))
        as avg_amount from ({})as merList left join ({})as lw on merList.merchant_id=lw.merchant_id left join ({})as ld
        on merList.merchant_id=ld.merchant_id'''.format(sql_merList.format(self.fenqi), LD_help_wechat, LD_help_dc)
        return LD_help_avg

    # 查询券配置id对应的标签名
    def cou_cfg_id2label(self, cou_cfg_id):
        sql = '''select label_name from labels, coupons_cfg_label_rela cl
              where labels.label_id=cl.label_id and coupons_config_id='{}';'''.format(cou_cfg_id)
        results = self.query(self.coupons, sql)
        labels = []
        for result in results:
            labels.append(result[0])
        return ';'.join(labels) if len(labels) > 0 else '无'

    # 商户id对应名称
    def mer_id2name(self):
        # sql = '''select short_name from merchant where merchant_id='{}';'''.format(merchant_id)
        # return self.query(self.fenqi, sql)[0][0]
        sql = '''select merchant_id, short_name from merchant'''
        result = self.query(self.fenqi, sql)
        dict = {}
        for pair in result:
            dict[pair[0]] = pair[1]
        return dict

    # 查找帮发券的邻店
    def get_LD(self, coupons_cfg_id, dict):
        sql = '''select distinct merchant_id from coupons, coupons_promote cp
        where coupons.coupons_promote_id=cp.coupons_promote_id and coupons_config_id='{}';'''.format(coupons_cfg_id)
        results = self.query(self.coupons, sql)
        LD = []
        for result in results:
            LD.append(dict[result[0]])
        return ';'.join(LD)

class Export:
    def __init__(self):
        self.connect = Connect()

    def shyq(self, start_date, end_date, dir_name, opt={}):
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
        if opt:
            _temp = ["{}='{}'".format(i,j) for i,j in opt.items() if i not in ('MERCHANT_ID','MERCHANT_TYPE')]
            _temp.extend(["merchant.{}='{}'".format(i,j) for i,j in opt.items() if i in ('MERCHANT_ID','MERCHANT_TYPE')])
            sql0 += ' AND ' + ' AND '.join(_temp)
        result0 = self.connect.query(self.connect.fenqi, sql0)
        res0 = {}
        dict_region = self.connect.region_code2name()
        mer = []  # mer是merchant_id的list
        for _mer in result0:
            res0[_mer[0]]=[dict_region[_mer[1]] if _mer[1]!=None and _mer[1]!=''else '-',
                         dict_region[_mer[2]] if _mer[2]!=None and _mer[2]!=''else '-',
                         _mer[3], _mer[4] if _mer[4]!=None and _mer[4]!=''else '-', _mer[5]if _mer[5]!=None and _mer[5]!=''else '-']
            mer.append(_mer[0])

        # 计算商户流水、消费笔数、客单价(分别计算微信消费记录、储值卡消费记录)
        sql_wechat = '''(select merchant_id, sum(amount)as sum1, count(*)as num1 from merchant, wechat_pay_log as wpl, user
        where merchant.merchant_config_id = user.merchant_config_id and user.user_id = wpl.user_id and wpl.state = 2 
        and wpl.type in (2,3) and wpl.create_time > '{}' and wpl.create_time < '{}' group by merchant_id)
        as pay1'''.format(start_date, end_date)
        sql_dc = '''(select merchant_id, sum(abs(amount))as sum2, count(*)as num2 from user_deposit_card as dc, 
        user_deposit_card_log as dcl where dc.user_deposit_card_id = dcl.user_deposit_card_id and amount < 0 and 
        dcl.create_time > '{}' and dcl.create_time < '{}' group by merchant_id)as pay2'''.format(start_date, end_date)
        sql_mer = '''(select merchant.merchant_id,merchant.short_name from subbranch, merchant 
        where subbranch.merchant_id=merchant.merchant_id and sub_type=1)as merList'''
        #办卡数、办卡金额（分别计算一次充和分期充）
        sql_onepay = '''select sum(amount)as sum1, count(*)as num1, merchant_id from wechat_pay_log wl, user, merchant where wl.state=2 
        and wl.type=1 and user.merchant_config_id=merchant.merchant_config_id and wl.user_id=user.user_id and wl.create_time>'{}' 
        and wl.create_time<'{}' group by merchant_id'''.format(start_date, end_date)
        sql_fenqi = '''select sum(expect_principal)as sum2, sum(if(r.current_term=1, 1, 0))as num2, merchant_id from user_deposit_card dc, 
        repayment r where dc.instalment_apply_id=r.apply_id and r.state=2 and r.actual_repayment_time>'{}' and r.actual_repayment_time<'{}' 
        group by dc.merchant_id'''.format(start_date, end_date)
        sql_recharge = '''(select merList.merchant_id,(ifnull(sum1,0)+ifnull(sum2,0))as recharge_total, (ifnull(num1,0)+ifnull(num2,0))
        as recharge_num from {} left join ({})as onepay on merList.merchant_id=onepay.merchant_id left join ({})as fenqi on 
        merList.merchant_id=fenqi.merchant_id)as recharge'''.format(sql_mer, sql_onepay, sql_fenqi)
        #汇总这五个数据，外加商户简称
        sql1 = '''select merList.merchant_id, short_name, (ifnull(sum1,0)+ifnull(sum2,0))as amount,(ifnull(num1,0)+ifnull(num2,0))as num,  
        recharge_num, recharge_total from {} left join {} on merList.merchant_id=pay1.merchant_id left join {} on merList.merchant_id=
        pay2.merchant_id left join {} on merList.merchant_id=recharge.merchant_id'''.format(sql_mer, sql_wechat, sql_dc, sql_recharge)
        result1 = self.connect.query(self.connect.fenqi, sql1)
        res1 = {}
        for _mer in result1:
            res1[_mer[0]] = [_mer[1],_mer[2],_mer[3],Decimal(_mer[2]/_mer[3]).quantize(Decimal("0.00")) if _mer[3]!=0 else Decimal("0.00"), int(_mer[4]), _mer[5]]
            #res1词典的key为merchant_id, value为 列表[商户简称、商户流水、消费笔数、客单价、办卡数、办卡金额]

        # 关注券GZ、促活券CH、邻店券LD统计
        GZ = '145556';CH = '145558'
        sql_coupons = '''select merchant_id, count(*)as num from coupons, coupons_cfg_label_rela as cl, coupons_config 
        where coupons.coupons_config_id=cl.coupons_config_id and coupons.coupons_config_id=coupons_config.coupons_config_id 
        and label_id = '{}' and coupons.create_time > '{}' and coupons.create_time < '{}' {} group by merchant_id;'''
        sql_launch = '''select merchant_id, count(*) from coupons_config, coupons_cfg_label_rela as cl where 
                coupons_config.coupons_config_id=cl.coupons_config_id and label_id='{}' and coupons_config.status=2 group by merchant_id;'''
        # get → 领券量；    use → 用券量；  launch → 上架种类数； avg → 客单价
        sql_GZ_get = sql_coupons.format(GZ, start_date, end_date, '')
        sql_GZ_use = sql_coupons.format(GZ, start_date, end_date, 'and coupons.status=1')
        sql_GZ_launch = sql_launch.format(GZ)
        sql_GZ_avg = self.connect.coupons_avg(GZ, start_date, end_date)
        sql_CH_get = sql_coupons.format(CH, start_date, end_date, '')
        sql_CH_use = sql_coupons.format(CH, start_date, end_date, 'and coupons.status=1')
        sql_CH_launch = sql_launch.format(CH)
        sql_CH_avg = self.connect.coupons_avg(CH, start_date, end_date)
        #邻店帮我发的券的统计
        LD_help = '''select merchant_id,count(*)as num from coupons, coupons_config where 
        coupons.coupons_config_id=coupons_config.coupons_config_id and coupons.{time}>'{start_time}' 
        and coupons.{time}<'{end_time}' and coupons.coupons_promote_id is not null group by merchant_id'''
        LD_help_get = LD_help.format(time='create_time', start_time=start_date, end_time=end_date)
        LD_help_use = LD_help.format(time='used_time', start_time=start_date, end_time=end_date)
        LD_help_avg = self.connect.getSQL_LD_avg(start_date, end_date)
        #我帮邻店发的券的统计
        help_LD = '''select merchant_id,count(*)as num from coupons, coupons_promote where 
        coupons.coupons_promote_id=coupons_promote.coupons_promote_id and coupons.{time}>'{start_time}' 
        and coupons.{time}<'{end_time}' group by merchant_id'''
        help_LD_get = help_LD.format(time='create_time', start_time=start_date, end_time=end_date)
        help_LD_use = help_LD.format(time='used_time', start_time=start_date, end_time=end_date)
        #汇总关注、促活、邻店券
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
                    if i == 3 or i ==7 or i == 9:
                        res2[_mer[0]][i] = round(_mer[1], 2)
                    else:
                        res2[_mer[0]][i] = _mer[1]

        #回头客
        sql_wechat = '''(select user_id, count(*)as num1 from wechat_pay_log where state = 2 and type in (2,3)
        and create_time > '{}' and create_time < '{}' group by user_id)as userw'''
        sql_dc = '''(select user_id, count(*)as num2 from user_deposit_card as dc, user_deposit_card_log as dcl
        where dc.user_deposit_card_id=dcl.user_deposit_card_id and amount<0 and dcl.create_time > '{}' and
        dcl.create_time < '{}' group by user_id)as userd'''
        sql_userList = '''(select user_id, merchant_id from user, merchant where user.merchant_config_id=
        merchant.merchant_config_id)as userList'''
        sql_total_num = '''select * from(select userList.user_id, ifnull(userw.num1,0)+ifnull(userd.num2,0)as num, userList.merchant_id from
        {} left join {} on userList.user_id = userw.user_id left join {} on userList.user_id = userd.user_id)as totalNum where num>0'''
        sql_firstUsr = '''select user_id from ({})as firUsrList'''.format(
            sql_total_num.format(sql_userList, sql_wechat.format('2016-1-1',start_date), sql_dc.format('2016-1-1',start_date)))
        sql_CurrUsr = sql_total_num.format(sql_userList, sql_wechat.format(start_date, end_date), sql_dc.format(start_date, end_date))
        sql_Usr = '''select user_id, if(user_id in ({}), num, num-1)as usr_num, merchant_id from ({})as curr'''.format(sql_firstUsr,sql_CurrUsr)
        sql = '''select merchant_id, sum(usr_num) from ({})as usrNum group by merchant_id'''.format(sql_Usr)
        result3 = self.connect.query(self.connect.fenqi, sql)
        res3 = {}    #res是商户id映射到回头客数的词典
        for _mer in result3:
            res3[_mer[0]] = int(_mer[1])

        for mID in mer:
            _data = []
            _data.append(res1[mID][0])  #商户简称
            _data.extend(res0[mID][0:5] if mID in res0 else ['-','-','-','-','-'])  #行政区、微区域、行业、销售姓名、运营姓名
            _data.extend(res1[mID][1:4])    #商户流水、消费笔数、客单价
            _data.extend(res2[mID][0:4])    #关注券
            _data.append('%.1f%%' % (res2[mID][1] / res2[mID][0] * 100) if res2[mID][0] > 0 else '0.0%')
            _data.extend(res2[mID][4:8])    #促活券
            _data.append('%.1f%%' % (res2[mID][5] / res2[mID][4] * 100) if res2[mID][4] > 0 else '0.0%')
            _data.extend(res2[mID][8:13])   #邻店券
            _data.extend([res3.get(mID, 0), res1[mID][4], res1[mID][5]])  #回头客、办卡数、办卡金额
            all_data.append(_data)
        
        df = pd.DataFrame(all_data,columns=columns)
        # df.to_csv(os.path.join(dir_name,'shyq.csv'),index=False,encoding='gbk',sep=',')
        return df, '商户用券详情'

    def qpm(self, start_date, end_date, dir_name, opt={}):
        columns = ['排名', '关注券名称', '关注券使用数', '关注券商户名称', '关注券标签', '关注券客单价',
                   '促活券名称', '促活券使用数', '促活券商户名称', '促活券标签', '促活券客单价',
                   '邻店券名称', '邻店券使用数', '邻店券的发券商户名称', '邻店券的用券商户名称',
                   '邻店券标签', '邻店券客单价']
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        all_data = []

        GZ = '145556';CH = '145558'
        sql_coupons = '''select cc.name, count(*) as num, merchant_id, cc.coupons_config_id from coupons, coupons_cfg_label_rela cl, coupons_config cc
        where coupons.coupons_config_id=cl.coupons_config_id and coupons.coupons_config_id=cc.coupons_config_id and label_id = '{}' and 
        coupons.create_time > '{}' and coupons.create_time < '{}' and coupons.status=1 group by cc.coupons_config_id order by num desc;'''
        # 关注券
        sql_GZ = sql_coupons.format(GZ, start_date, end_date)
        result_GZ1 = self.connect.query(self.connect.coupons, sql_GZ)
        sql_GZ_avg = self.connect.coupons_avg(GZ, start_date, end_date)
        result_GZ2 = self.connect.query('', sql_GZ_avg)
        GZ_avg = {}
        for m in result_GZ2:
            GZ_avg[m[0]]=round(m[1], 2)
        # 促活券
        sql_CH = sql_coupons.format(CH, start_date, end_date)
        result_CH1 = self.connect.query(self.connect.coupons, sql_CH)
        sql_CH_avg = self.connect.coupons_avg(CH, start_date, end_date)
        result_CH2 = self.connect.query('', sql_CH_avg)
        CH_avg = {}
        for m in result_CH2:
            CH_avg[m[0]]=round(m[1], 2)
        # 邻店券
        sql_LD = '''select cc.name,count(*)as num, merchant_id, cc.coupons_config_id from coupons, coupons_config cc where 
        coupons.coupons_config_id=cc.coupons_config_id and coupons.status=1 and coupons.used_time>'{}' and coupons.used_time<'{}' 
        and coupons.coupons_promote_id is not null group by cc.coupons_config_id order by num desc'''
        result_LD1 = self.connect.query(self.connect.coupons, sql_LD.format(start_date, end_date))
        sql_LD_avg = self.connect.getSQL_LD_avg(start_date, end_date)
        result_LD2 = self.connect.query('', sql_LD_avg)
        LD_avg = {}
        for m in result_LD2:
            LD_avg[m[0]]=round(m[1], 2)

        dict_id2name = self.connect.mer_id2name()
        for i in range(10):
            _data = []
            _data.append("TOP{}".format(i+1))
            if i < len(result_GZ1):
                _data.extend(result_GZ1[i][0:2])
                _data.extend([dict_id2name[result_GZ1[i][2]], self.connect.cou_cfg_id2label(result_GZ1[i][-1]),
                              GZ_avg[result_GZ1[i][2]]])   #商户名称、标签、客单价
            else:
                _data.extend(['-', '-', '-', '-', '-'])
            if i < len(result_CH1):
                _data.extend(result_CH1[i][0:2])
                _data.extend([dict_id2name[result_CH1[i][2]], self.connect.cou_cfg_id2label(result_CH1[i][-1]),
                              GZ_avg[result_CH1[i][2]]])
            else:
                _data.extend(['-', '-', '-', '-', '-'])
            if i < len(result_LD1):
                _data.extend(result_LD1[i][0:2])
                _data.extend([self.connect.get_LD(result_LD1[i][-1], dict_id2name), dict_id2name[result_LD1[i][2]],
                              self.connect.cou_cfg_id2label(result_LD1[i][-1]), LD_avg[result_LD1[i][2]]])
            else:
                _data.extend(['-', '-', '-', '-', '-', '-'])
            all_data.append(_data)
            # print(all_data)
        df = pd.DataFrame(all_data, columns=columns)
        # df.to_csv(os.path.join(dir_name, 'qpm.csv'), index=False, encoding='gbk', sep=',')
        return df, '券排名'

    def ydqxq(self, start_date, end_date, dir_name, opt={}):
        columns = ['日期', '名称', '商户', '标签', '起始日期之前的领券量', '截止日期之前的领券量', '发放结束日期']
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        all_data1 = [];all_data2 = [];all_data3 = [];   #快到期、修改、下线
        sql_coupons_num = '''select count(*) from coupons where create_time<'{}' and coupons_config_id='{}';'''
        dict_id2name = self.connect.mer_id2name()
        #快到期
        for i in range((end_date-start_date).days):
            curr_date = start_date + datetime.timedelta(i)  #不含当天,当天零时
            sql_kdq = '''select name, merchant_id, coupons_config_id, publish_end_date from coupons_config 
            where expire_date is not null and datediff(expire_date,'{}')=10'''.format(curr_date)
            result = self.connect.query(self.connect.coupons, sql_kdq)
            for x in range(len(result)):
                # curr_date2 = start_date + datetime.timedelta(i+1)   #含当天,次日零时 算表的日期之前的领券量可用
                sql_kdq_num = sql_coupons_num.format(start_date, result[x][2])
                get_num = self.connect.query(self.connect.coupons, sql_kdq_num)[0][0]
                sql_kdq_num2 = sql_coupons_num.format(end_date, result[x][2])
                get_num2 = self.connect.query(self.connect.coupons, sql_kdq_num2)[0][0]
                all_data1.append([curr_date.strftime("%y%m%d"), result[x][0], dict_id2name[result[x][1]],
                              self.connect.cou_cfg_id2label(result[x][2]), get_num, get_num2, result[x][3].strftime("%y%m%d")])
        #修改
        sql_xg = '''select update_time, name, merchant_id, coupons_config_id, publish_end_date 
        from coupons_config where update_time > '{}' and update_time < '{}';'''.format(start_date, end_date)
        result = self.connect.query(self.connect.coupons, sql_xg)
        for res in result:
            sql_xg = sql_coupons_num.format(start_date, res[3])
            get_num = self.connect.query(self.connect.coupons, sql_xg)[0][0]
            sql_xg = sql_coupons_num.format(end_date, res[3])
            get_num2 = self.connect.query(self.connect.coupons, sql_xg)[0][0]
            all_data2.append([res[0].strftime("%y%m%d"), res[1], dict_id2name[res[2]],
                              self.connect.cou_cfg_id2label(res[3]),get_num, get_num2, res[4].strftime("%y%m%d")])
        #下线
        sql_xx = '''select publish_end_date, name, merchant_id, coupons_config_id from coupons_config 
        where publish_end_date>'{}' and publish_end_date<'{}';'''.format(start_date, end_date)
        result = self.connect.query(self.connect.coupons, sql_xx)
        for res in result:
            sql_xx = sql_coupons_num.format(start_date, res[3])
            get_num = self.connect.query(self.connect.coupons, sql_xx)[0][0]
            sql_xx = sql_coupons_num.format(end_date, res[3])
            get_num2 = self.connect.query(self.connect.coupons, sql_xx)[0][0]
            all_data3.append([res[0].strftime("%y%m%d"), res[1], dict_id2name[res[2]],
                              self.connect.cou_cfg_id2label(res[3]), get_num, get_num2, res[0].strftime("%y%m%d")])

        all_data = [all_data1, all_data2, all_data3];   all_df = []
        file = ['快到期券详情', '修改券详情', '下线券详情']
        # i = 0
        for d in all_data:
            df = pd.DataFrame(d, columns=columns)
            all_df.append(df)
            # df.to_csv(os.path.join(dir_name, file[i]), index=False, encoding='gbk', sep=',')
            # i += 1
        return all_df, file

def main():
    export = Export()
    # opt = {'MERCHANT_ID':'yifanmeirongMerchant'}
    # opt = {'MERCHANT_TYPE':1}
    export.shyq('2018-6-20','2018-7-21','./', opt={})
    # export.qpm('2018-7-1','2018-7-21','./')
    # export.ydqxq('2018-6-1', '2018-7-16', './')

if __name__ == '__main__':
    main()