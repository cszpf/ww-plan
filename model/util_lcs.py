# encoding=utf-8
import MySQLdb
import datetime
import os
import pandas as pd
import connectTool

label_field = [ '关注券','促活券','邻店券','基础券','节日券','周末券','活动券','套餐券','提额券']
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
    def khhz(self, start_date, end_date, dir_name, opt={}):
        # start_date:形如"2018-xx-xx"的str
        # end_date:形如"2018-xx-xx"的str
        # dir_name:存放门店流水表的目标文件夹
        columns = ['指标', '行政区',  '微区域', '行业', '销售姓名', '运营姓名']
        all_data = []
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        for i in range((end_date - start_date).days):
            x = start_date + datetime.timedelta(i)
            columns.append(x.strftime("%y%m%d"))

        sql = """SELECT subbranch_id,ADMIN_REGION_CODE,MICRO_REGION_CODE,merchant_type_name,SALE_NAME, OPERATOR_NAME,a.merchant_id,b.create_time
                  FROM subbranch a,merchant b, merchant_industry c
                  WHERE a.merchant_id=b.merchant_id AND b.merchant_type = c.merchant_type AND a.create_time IS NOT NULL"""
        if opt:
            _temp = ["{}='{}'".format(i, j) for i, j in opt.items() if i not in ('MERCHANT_ID', 'MERCHANT_TYPE')]
            _temp.extend(["b.{}='{}'".format(i, j)  for i, j in opt.items() if i in ('MERCHANT_ID', 'MERCHANT_TYPE')])
            sql += ' AND ' + ' AND '.join(_temp)
        result = self.connect.query(self.connect.fenqi, sql)
        #print(result)
        #print(len(result))
        data_qqd = []
        if opt.get('ADMIN_REGION_CODE','-')!='-':
            data_qqd.append(self.connect.region_code2name(opt.get('ADMIN_REGION_CODE')))
        else:
            data_qqd.append('-')
        if opt.get('MICRO_REGION_CODE','-')!='-':
            data_qqd.append(self.connect.region_code2name(opt.get('MICRO_REGION_CODE')))
        else:
            data_qqd.append('-')
        if opt.get('MERCHANT_TYPE','-')!='-':
            data_qqd.append(opt.get('SALE_NAME'))
        else:
            data_qqd.append('-')
        if opt.get('SALE_NAME','-')!='-':
            data_qqd.append(opt.get('SALE_NAME'))
        else:
            data_qqd.append('-')
        if opt.get('OPERATOR_NAME','-')!='-':
            data_qqd.append(opt.get('SALE_NAME'))
        else:
            data_qqd.append('-')
        #print(data_qqd)
        result2=();result3=();result4=();result7=();result10=();result1=set()
        for all_sub in result:
            if all_sub:
                all_sub=list(all_sub)
                result1.add((all_sub[6],all_sub[7]))

                sql2 = """SELECT subbranch_id,create_time
                                          FROM subbranch 
                                          WHERE state=2 AND subbranch_id='{}'""".format(all_sub[0])
                result22 = self.connect.query(self.connect.fenqi, sql2)
                result2 = result2 + result22
                #关注客户数
                sql3 = """SELECT user_id,a.create_time
                                          FROM user a,merchant_config b,subbranch c
                                          WHERE a.merchant_config_id=b.merchant_config_id AND b.merchant_config_id=c.merchant_config_id AND c.sub_type=1 
                                                 AND c.state=2 AND c.subbranch_id='{}'""".format(all_sub[0])
                result33 = self.connect.query(self.connect.fenqi, sql3)
                result3 = result3 + result33
                #活跃、流失客户数
                sql4 = """SELECT a.user_id,a.create_time,c.create_time,d.create_time
                                          FROM user a,user_deposit_card b,user_deposit_card_log c,wechat_pay_log d
                                          WHERE a.user_id=b.user_id AND b.user_deposit_card_id=c.user_deposit_card_id AND a.user_id=d.user_id 
                                                 AND c.subbranch_id='{}'""".format(all_sub[0])
                result44 = self.connect.query(self.connect.fenqi, sql4)
                result4 = result4 + result44
                #复购次数
                sql5 = """SELECT a.user_id,a.create_time,c.create_time
                                          FROM user a,user_deposit_card b,user_deposit_card_log c
                                          WHERE a.user_id=b.user_id AND b.user_deposit_card_id=c.user_deposit_card_id AND c.subbranch_id='{}'""".format(
                    all_sub[0])
                result5 = self.connect.query(self.connect.fenqi, sql5)
                sql6 = """SELECT a.user_id,a.create_time,d.create_time
                                          FROM user a,wechat_pay_log d
                                          WHERE  a.user_id=d.user_id AND d.subbranch_id='{}' """.format(all_sub[0])
                result6 = self.connect.query(self.connect.fenqi, sql6)
                result7 = result7 + result5 + result6
                #print(result7)
                #标签券
                sql8 = """SELECT a.coupons_promote_id,c.create_time,c.amount,e.label_id
                          FROM coupons.coupons a,coupons.coupons_log b,fenqi.wechat_pay_log c,coupons.coupons_cfg_label_rela e
                          WHERE  a.coupons_id=b.coupons_id AND b.wechat_pay_log_id=c.wechat_pay_log_id 
                                 AND a.coupons_config_id=e.coupons_config_id AND c.subbranch_id='{}'""".format(all_sub[0])
                result8 = self.connect.query('', sql8)
                #邻店券
                sql9 = """SELECT a.coupons_promote_id,d.create_time,d.amount,e.label_id
                          FROM coupons.coupons a,coupons.coupons_log b,fenqi.user_deposit_card_log d,coupons.coupons_cfg_label_rela e
                          WHERE  a.coupons_id=b.coupons_id AND b.user_deposit_card_log_id=d.user_deposit_card_id 
                                  AND a.coupons_config_id=e.coupons_config_id AND d.subbranch_id='{}'""".format(all_sub[0])
                result9 = self.connect.query('', sql9)
                result10=result10 + result8 + result9
        #print(result10)

        new_merchant_data = []
        merchant_data=[]
        new_subbranch_data = []
        subbranch_data=[]
        new_user_data = []
        user_data=[]
        new_positive_data=[]
        new_negative_data=[]
        repurchase_data=[]
        average_repurchase_data=[]
        new_neighbor_data=[]
        neighbor_data=[]
        new_attention_data=[]
        attention_data = []
        new_promote_data=[]
        promote_data=[]
        new_neighbor1_data=[]
        neighbor1_data=[]
        new_merchant_data.extend(['新增商户数']);new_merchant_data.extend(data_qqd)
        merchant_data.extend(['累计商户数']);merchant_data.extend(data_qqd)
        new_subbranch_data.extend(['新增门店数']);new_subbranch_data.extend(data_qqd)
        subbranch_data.extend(['累计门店数']);subbranch_data.extend(data_qqd)
        new_user_data.extend(['新增关注客户数']);new_user_data.extend(data_qqd)
        user_data.extend(['累计关注客户数']);user_data.extend(data_qqd)
        new_positive_data.extend(['新增活跃客户数']);new_positive_data.extend(data_qqd)
        new_negative_data.extend(['新增流失客户数']);new_negative_data.extend(data_qqd)
        repurchase_data.extend(['复购次数']);repurchase_data.extend(data_qqd)
        average_repurchase_data.extend(['回头客的平均复购周期']);average_repurchase_data.extend(data_qqd)
        new_neighbor_data.extend(['新增邻店带客数']);new_neighbor_data.extend(data_qqd)
        neighbor_data.extend(['累计邻店带客数']);neighbor_data.extend(data_qqd)
        new_attention_data.extend(['新增关注券消费的客单价']);new_attention_data.extend(data_qqd)
        attention_data.extend(['累计关注券消费的客单价']);attention_data.extend(data_qqd)
        new_promote_data.extend(['新增促活券消费的客单价']);new_promote_data.extend(data_qqd)
        promote_data.extend(['累计促活券消费的客单价']);promote_data.extend(data_qqd)
        new_neighbor1_data.extend(['新增邻店券消费的客单价']);new_neighbor1_data.extend(data_qqd)
        neighbor1_data.extend(['累计邻店券消费的客单价']);neighbor1_data.extend(data_qqd)

        for i in range((end_date - start_date).days):
            data={}
            repurchase_id_list=[]
            x = start_date + datetime.timedelta(i)
            count_new_merchant=0
            count_merchant=0
            count_new_subbranch = 0
            count_subbranch=0
            count_new_user = 0
            count_user=0
            new_positive=set()
            new_negative=set()
            count_repurchase=0
            count_average_repurchase=0
            count_purchase=0
            count_new_neighbor=0
            count_neighbor=0
            count_new_attention=0
            count_attention=0
            count_att=0
            count_new_promote=0
            count_promote=0
            count_pro=0
            count_new_neighbor1=0
            count_neighbor1 = 0
            count_neigh=0

            #商户数
            for _sub in result1:
                if _sub[1]:
                    if _sub[1].date()==x:
                        count_new_merchant+=1
                    if _sub[1].date()<=x:
                        count_merchant+=1
            #门店数
            for _sub in result2:
                if _sub[1]:
                    if _sub[1].date()==x:
                        count_new_subbranch+=1
                    if _sub[1].date()<=x:
                        count_subbranch+=1
            #用户数
            for _sub in result3:
                if _sub[1]:
                    if _sub[1].date()==x:
                        count_new_user+=1
                    if _sub[1].date()<=x:
                        count_user+=1
            #活跃、流失客户数
            for _sub in result4:
                if _sub[2].date()<=x and _sub[2].date()>=x-datetime.timedelta(30):
                    new_positive.add(_sub[0])
                if _sub[3].date()<=x and _sub[2].date()>=x-datetime.timedelta(30):
                    new_positive.add(_sub[0])
                if _sub[2].date()<=x-datetime.timedelta(60):
                    new_negative.add(_sub[0])
                if _sub[2].date()>=x-datetime.timedelta(30):
                    new_negative.add(_sub[0])
            #复购次数
            for _sub in result7:
                if _sub[2].date()==x:
                    count_purchase+=1#指定日期的消费次数
                    if _sub[0] in data.keys():
                        data[_sub[0]]+=1
                    else:
                        data[_sub[0]]=1
                       #data:指定日期的客户{用户ID：消费次数}
            #print(data)
            for _sub in data.values():
                #print(_sub)
                if _sub!=1:
                    count_repurchase=count_repurchase+_sub
            #当天回头客的平均复购周期
            for id in data.keys():
                min=0
                for _sub in result7:
                    if _sub[0]==id:
                        if (x-_sub[2].date()).days>=0:#回头客
                            if min==0:
                                min = (x - _sub[2].date()).days
                            if min>((x-_sub[2].date()).days):
                                min=(x-_sub[2].date()).days
                count_average_repurchase+=min
            if len(data.keys())==0:
                count_average_repurchase=0
            else:
                count_average_repurchase=int(count_average_repurchase/len(data.keys()))
            #新增、累计邻店带客数
            for _sub in result10:
                if _sub[0] != '':
                    if _sub[1].date()==x :
                        count_new_neighbor+=1
                    if _sub[1].date()<=x :
                        count_neighbor+=1
            #新增、累计关注券消费的客单价
            GZ = '145556'
            CH = '145558'
            for _sub in result10:
                if _sub[3] == '145556':
                    if _sub[1].date()==x :
                        count_new_attention+=_sub[2]
                    if _sub[1].date()<=x :
                        count_attention += _sub[2]
                        count_att += 1
            if count_att!=0:
                count_new_attention=count_new_attention/count_att
                count_attention=count_attention/count_att
            else:
                count_new_attention=0
                count_attention=0
            # 新增、累计促活券消费的客单价
            GZ = '145556'
            CH = '145558'
            for _sub in result10:
                if _sub[3] == '145558':
                    if _sub[1].date() == x :
                        count_new_promote += _sub[2]
                    if _sub[1].date() <= x :
                        count_promote += _sub[2]
                        count_pro += 1
            if count_pro!=0:
                count_new_promote = count_new_promote / count_pro
                count_promote = count_promote / count_pro
            else:
                count_new_promote =0
                count_promote = 0
            # 新增、累计邻店券消费的客单价
            for _sub in result10:
                if _sub[0] != '':
                    if _sub[1].date() == x :
                        count_new_neighbor1 += _sub[2]
                    if _sub[1].date() <= x :
                        count_neighbor1+= _sub[2]
                        count_neigh += 1
            if count_neigh!=0:
                count_new_neighbor1 = count_new_neighbor1 / count_neigh
                count_neighbor1 = count_neighbor1 / count_neigh
            else:
                count_new_neighbor1 = 0
                count_neighbor1 = 0


            new_merchant_data.append(count_new_merchant)
            merchant_data.append(count_merchant)
            new_subbranch_data.append(count_new_subbranch)
            subbranch_data.append(count_subbranch)
            new_user_data.append(count_new_user)
            user_data.append(count_user)
            new_positive_data.append(len(new_positive))
            new_negative_data.append(len(new_negative))
            repurchase_data.append(count_repurchase)
            average_repurchase_data.append(count_average_repurchase)
            new_neighbor_data.append(count_new_neighbor)
            neighbor_data.append(count_neighbor)
            new_attention_data.append(count_new_attention)
            attention_data.append(count_attention)
            new_promote_data.append(count_new_promote)
            promote_data.append(count_promote)
            new_neighbor1_data.append(count_new_neighbor1)
            neighbor1_data.append(count_neighbor1)

        all_data.append(new_merchant_data)
        all_data.append(merchant_data)
        all_data.append(new_subbranch_data)
        all_data.append(subbranch_data)
        all_data.append(new_user_data)
        all_data.append(user_data)
        all_data.append(new_positive_data)
        all_data.append(new_negative_data)
        all_data.append(repurchase_data)
        all_data.append(average_repurchase_data)
        all_data.append(new_neighbor_data)
        all_data.append(neighbor_data)
        all_data.append(new_attention_data)
        all_data.append(attention_data)
        all_data.append(new_promote_data)
        all_data.append(promote_data)
        all_data.append(new_neighbor1_data)
        all_data.append(neighbor1_data)
        # print(all_data)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data, columns=columns)
        # df.to_csv(os.path.join(dir_name, 'khhz.csv'), index=False, encoding='gbk', sep=',')
        return df, '客户汇总'

    # 实现卷汇总表的在线生成
    def qhz(self, start_date, end_date, dir_name, opt={}):
        # start_date:形如"2018-xx-xx"的str
        # end_date:形如"2018-xx-xx"的str
        # dir_name:存放门店流水表的目标文件夹
        columns = ['指标','微区域', '行业', '销售姓名', '运营姓名']
        all_data = []
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        for i in range((end_date - start_date).days):
            x = start_date + datetime.timedelta(i)
            columns.append(x.strftime("%y%m%d"))
        sql = """SELECT subbranch_id,MICRO_REGION_CODE,merchant_type_name,SALE_NAME, OPERATOR_NAME,a.merchant_id
                          FROM subbranch a,merchant b, merchant_industry c
                          WHERE a.merchant_id=b.merchant_id AND b.merchant_type = c.merchant_type AND a.create_time IS NOT NULL  """
        if opt:
            _temp = ["{}='{}'".format(i, j) for i, j in opt.items() if i not in ('MERCHANT_ID', 'MERCHANT_TYPE')]
            _temp.extend(["b.{}='{}'".format(i, j) for i, j in opt.items() if i in ('MERCHANT_ID', 'MERCHANT_TYPE')])
            sql += ' AND ' + ' AND '.join(_temp)
        result1 = self.connect.query(self.connect.fenqi, sql)
        # print(result1)
        # print(len(result1))
        data_qqd = []
        if opt.get('MICRO_REGION_CODE', '-') != '-':
            data_qqd.append(self.connect.region_code2name(opt.get('MICRO_REGION_CODE')))
        else:
            data_qqd.append('-')
        if opt.get('MERCHANT_TYPE', '-') != '-':
            data_qqd.append(opt.get('SALE_NAME'))
        else:
            data_qqd.append('-')
        if opt.get('SALE_NAME', '-') != '-':
            data_qqd.append(opt.get('SALE_NAME'))
        else:
            data_qqd.append('-')
        if opt.get('OPERATOR_NAME', '-') != '-':
            data_qqd.append(opt.get('SALE_NAME'))
        else:
            data_qqd.append('-')
        # print(data_qqd)
        result_label = ()
        result = ()
        if opt:
            for all_sub in result1:
                if all_sub:
                    all_sub = list(all_sub)
                    sql1 = """SELECT a.coupons_id,a.status,a.expire_date,a.create_time,b.status,update_time,b.subbranch_id
                         FROM coupons a,coupons_config b
                         WHERE a.coupons_config_id=b.coupons_config_id AND b.subbranch_id='{}'""".format(all_sub[0])
                    result = self.connect.query(self.connect.coupons, sql1)
                    sql2 = """SELECT coupons_id,a.status,a.expire_date,a.create_time,b.status,update_time,label_name,b.create_time,coupons_promote_id
                    FROM coupons a,coupons_config b,coupons_cfg_label_rela c,labels d
                    WHERE a.coupons_config_id=b.coupons_config_id AND a.coupons_config_id=c.coupons_config_id AND c.label_id=d.label_id 
                          AND b.subbranch_id='{}'""".format(all_sub[0])
                    result2 = self.connect.query(self.connect.coupons, sql2)
                    result_label = result_label + result2
        else:
            sql1="""SELECT a.coupons_id,a.status,a.expire_date,a.create_time,b.status,update_time,b.subbranch_id
                FROM coupons a,coupons_config b
                WHERE a.coupons_config_id=b.coupons_config_id"""
            result= self.connect.query(self.connect.coupons, sql1)
            sql2 = """SELECT coupons_id,a.status,a.expire_date,a.create_time,b.status,update_time,label_name,b.create_time,coupons_promote_id
            FROM coupons a,coupons_config b,coupons_cfg_label_rela c,labels d
            WHERE a.coupons_config_id=b.coupons_config_id AND a.coupons_config_id=c.coupons_config_id AND c.label_id=d.label_id """
            result_label = self.connect.query(self.connect.coupons, sql2)
        #print(result)
        #领券数
        _data = []
        used_data=[]
        out_time_data=[]
        downline_data=[]
        modify_data=[]
        expire_data=[]
        #关注券
        add_attention_data=[]
        attention_data=[]
        used_attention_data=[]
        attention_rate=[]
        expire_attention_data=[]
        #促活券
        add_promote_data=[]
        promote_data=[]
        used_promote_data=[]
        expire_promote_data=[]
        #邻店券
        add_neighbor_data=[]
        neighbor_data=[]
        used_neighbor_data=[]
        expire_neighbor_data=[]
        #基础券
        add_basis_data=[]
        basis_data=[]
        used_basis_data=[]
        expire_basis_data=[]
        #场景券
        add_scene_data=[]
        scene_data=[]
        used_scene_data=[]
        expire_scene_data=[]

        _data.extend(['领券数']);_data.extend(data_qqd)
        used_data.extend(['用券数']);used_data.extend(data_qqd)
        out_time_data.extend(['失效券数']);out_time_data.extend(data_qqd)
        downline_data.extend(['下线券数']);downline_data.extend(data_qqd)
        modify_data.extend(['修改券数']);modify_data.extend(data_qqd)
        expire_data.extend(['快到期券数']);expire_data.extend(data_qqd)
        add_attention_data.extend(['新增关注券数']);add_attention_data.extend(data_qqd)
        attention_data.extend(['关注券领券数']);attention_data.extend(data_qqd)
        used_attention_data.extend(['关注券用券数']);used_attention_data.extend(data_qqd)
        attention_rate.extend(['关注券用券率']);attention_rate.extend(data_qqd)
        expire_attention_data.extend(['关注券失效数']);expire_attention_data.extend(data_qqd)
        add_promote_data.extend(['新增促活券数']);add_promote_data.extend(data_qqd)
        promote_data.extend(['促活券领券数']);promote_data.extend(data_qqd)
        used_promote_data.extend(['促活券用券数']);used_promote_data.extend(data_qqd)
        expire_promote_data.extend(['促活券失效数']);expire_promote_data.extend(data_qqd)
        add_neighbor_data.extend(['新增邻店券数']);add_neighbor_data.extend(data_qqd)
        neighbor_data.extend(['邻店券领券数']);neighbor_data.extend(data_qqd)
        used_neighbor_data.extend(['邻店券用券数']);used_neighbor_data.extend(data_qqd)
        expire_neighbor_data.extend(['邻店券失效数']);expire_neighbor_data.extend(data_qqd)
        add_basis_data.extend(['新增基础券数']);add_basis_data.extend(data_qqd)
        basis_data.extend(['基础券领券数']);basis_data.extend(data_qqd)
        used_basis_data.extend(['基础券用券数']);used_basis_data.extend(data_qqd)
        expire_basis_data.extend(['基础券失效数']); expire_basis_data.extend(data_qqd)
        add_scene_data.extend(['新增场景券数']);add_scene_data.extend(data_qqd)
        scene_data.extend(['场景券领券数']);scene_data.extend(data_qqd)
        used_scene_data.extend(['场景券用券数']);used_scene_data.extend(data_qqd)
        expire_scene_data.extend(['场景券失效数']);expire_scene_data.extend(data_qqd)


        for i in range((end_date - start_date).days):
            x = start_date + datetime.timedelta(i)
            count = 0
            count_used = 0
            count_out_time = 0
            count_downline = 0
            count_modify = 0
            count_expire = 0
            count_attention_rate=0
            #关注卷
            count_add_attention = 0
            count_attention=0
            count_used_attention=0
            count_expire_attention=0
            #促活卷
            count_add_promote = 0
            count_promote=0
            count_used_promote=0
            count_expire_promote=0
            #邻店卷
            count_add_neighbor = 0
            count_neighbor=0
            count_used_neighbor=0
            count_expire_neighbor=0
            #基础卷
            count_add_basis = 0
            count_basis=0
            count_used_basis=0
            count_expire_basis=0
            #场景卷
            count_add_scene = 0
            count_scene=0
            count_used_scene=0
            count_expire_scene=0

            for _sub in result:
                if _sub[3].date()<=x:
                    count+=1
                    if _sub[1]==1:
                        count_used+=1
                    if _sub[1]==2:
                        count_out_time+=1
                    if _sub[2]-datetime.timedelta(10)<x:
                        count_expire+=1
                    if _sub[4]==3:
                        count_downline+=1
                    if _sub[5].date()<=x:
                        count_modify+=1
                    #关注券
            for _sub in result_label:
                if _sub[3].date() == x:
                    if _sub[6] == label_field[0]:
                        count_attention += 1
                        if _sub[1]==1:
                            count_used_attention+=1
                        if _sub[1]==2:
                            count_expire_attention+=1
                    if _sub[6] == label_field[1]:
                        count_promote += 1
                        if _sub[1]==1:
                            count_used_promote+=1
                        if _sub[1]==2:
                            count_expire_promote+=1
                    #邻店券
                    if _sub[8] != '':
                        count_neighbor += 1
                        if _sub[1]==1:
                            count_used_neighbor+=1
                        if _sub[1]==2:
                            count_expire_neighbor+=1
                    if _sub[6] == label_field[3]:
                        count_basis += 1
                        if _sub[1]==1:
                            count_used_basis+=1
                        if _sub[1]==2:
                            count_expire_basis+=1
                    if _sub[6] == label_field[4] or label_field[5] or label_field[6] or label_field[7] or label_field[8]:
                        count_scene += 1
                        if _sub[1]==1:
                            count_used_scene+=1
                        if _sub[1]==2:
                            count_expire_scene+=1
                if _sub[6]==label_field[0] and _sub[7].date()==x:
                    count_add_attention+=1
                if _sub[6]==label_field[1] and _sub[7].date()==x:
                    count_add_promote+=1
                if _sub[8]!='' and _sub[7].date()==x:
                    count_add_neighbor+=1
                if _sub[6]==label_field[3] and _sub[7].date()==x:
                    count_add_basis += 1
                #新增场景券
                if _sub[7].date()==x:
                    if _sub[6]==label_field[4]:
                       count_add_scene += 1
                    if _sub[6] == label_field[7]:
                       count_add_scene += 1
                    if _sub[6] == label_field[5]:
                       count_add_scene += 1
                    if _sub[6] == label_field[6]:
                       count_add_scene += 1
                    if _sub[6] == label_field[8]:
                       count_add_scene += 1
                if count_used_attention!=0:
                    count_attention_rate=count_used_attention/count_attention
                    count_attention_rate = format(count_attention_rate, '.1%')
                else:
                    count_attention_rate='-'
            #print(count_add_scene)
            _data.append(count)
            used_data.append(count_used)
            out_time_data.append(count_out_time)
            downline_data.append(count_downline)
            modify_data.append(count_modify)
            expire_data.append(count_expire)
            #关注卷
            add_attention_data.append(count_add_attention)
            attention_data.append(count_attention)
            used_attention_data.append(count_used_attention)
            attention_rate.append(count_attention_rate)
            expire_attention_data.append(count_expire_attention)
            #促活卷
            add_promote_data.append(count_add_promote)
            promote_data.append(count_promote)
            used_promote_data.append(count_used_promote)
            expire_promote_data.append(count_expire_promote)
            #邻店卷
            add_neighbor_data.append(count_add_neighbor)
            neighbor_data.append(count_neighbor)
            used_neighbor_data.append(count_used_neighbor)
            expire_neighbor_data.append(count_expire_neighbor)
            #基础卷
            add_basis_data.append(count_add_basis)
            basis_data.append(count_basis)
            used_basis_data.append(count_used_basis)
            expire_basis_data.append(count_expire_basis)
            #场景卷
            add_scene_data.append(count_add_scene)
            scene_data.append(count_scene)
            used_scene_data.append(count_used_scene)
            expire_scene_data.append(count_expire_scene)


        all_data.append(_data)
        all_data.append( used_data)
        all_data.append(out_time_data)
        all_data.append(downline_data)
        all_data.append(modify_data)
        all_data.append(expire_data)
        #关注卷
        all_data.append(add_attention_data)
        all_data.append(attention_data)
        all_data.append(used_attention_data)
        all_data.append(attention_rate)
        all_data.append(expire_attention_data)
        #促活卷
        all_data.append(add_promote_data)
        all_data.append(promote_data)
        all_data.append(used_promote_data)
        all_data.append(expire_promote_data)
        #促活卷
        all_data.append(add_neighbor_data)
        all_data.append(neighbor_data)
        all_data.append(used_neighbor_data)
        all_data.append(expire_neighbor_data)
        #基础卷
        all_data.append(add_basis_data)
        all_data.append(basis_data)
        all_data.append(used_basis_data)
        all_data.append(expire_basis_data)
        #场景卷
        all_data.append(add_scene_data)
        all_data.append(scene_data)
        all_data.append(used_scene_data)
        all_data.append(expire_scene_data)
        #print(all_data)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df = pd.DataFrame(all_data, columns=columns)
        # df.to_csv(os.path.join(dir_name, 'qhz.csv'), index=False, encoding='gbk', sep=',')
        return df, '券汇总'

def main():
    export = Export()
    opt = {
    'ADMIN_REGION_CODE':'2100'
    }
    #opt={}

    print(export.khhz('2018-8-20','2018-8-23','./', opt)[0])
    #print(export.qhz('2018-7-10', '2018-7-15', './', opt)[0])
if __name__ == '__main__':
    main()