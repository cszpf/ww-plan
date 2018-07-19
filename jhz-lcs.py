import MySQLdb
import datetime
import os
import pandas as pd

cwd = os.getcwd()
label_field = [ '关注券','促活券','邻店券','基础券','节日券','周末券','活动券','套餐券','提额券']


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


class Export:
    def __init__(self):
        self.connect = Connect()

    # 实现卷汇总表的在线生成
    def jhz(self, start_date, end_date, dir_name):
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

        sql1 = """SELECT coupons_id,a.status,a.expire_date,a.create_time,b.status,update_time,label_name,b.create_time,coupons_promote_id
        FROM coupons a,coupons_config b,coupons_cfg_label_rela c,labels d
        WHERE a.coupons_config_id=b.coupons_config_id AND a.coupons_config_id=c.coupons_config_id AND c.label_id=d.label_id"""
        result = self.connect.query(self.connect.coupons, sql1)
        #print(result)
        #领卷数
        _data = []
        used_data=[]
        out_time_data=[]
        downline_data=[]
        modify_data=[]
        expire_data=[]
        #关注卷
        add_attention_data=[]
        attention_data=[]
        used_attention_data=[]
        attention_rate=[]
        expire_attention_data=[]
        #促活卷
        add_promote_data=[]
        promote_data=[]
        used_promote_data=[]
        expire_promote_data=[]
        #邻店卷
        add_neighbor_data=[]
        neighbor_data=[]
        used_neighbor_data=[]
        expire_neighbor_data=[]
        #基础卷
        add_basis_data=[]
        basis_data=[]
        used_basis_data=[]
        expire_basis_data=[]
        #场景卷
        add_scene_data=[]
        scene_data=[]
        used_scene_data=[]
        expire_scene_data=[]

        _data.extend(['领券数','-',  '-', '-', '-'])
        used_data.extend(['用券数','-',  '-', '-', '-'])
        out_time_data.extend(['失效券数','-', '-', '-', '-'])
        downline_data.extend(['下线券数','-', '-', '-', '-'])
        modify_data.extend(['修改券数','-', '-', '-', '-'])
        expire_data.extend(['快到期券数','-', '-', '-', '-'])
        add_attention_data.extend(['新增关注卷数','-', '-', '-', '-'])
        attention_data.extend(['关注卷领卷数','-', '-', '-', '-'])
        used_attention_data.extend(['关注卷用卷数', '-', '-', '-', '-'])
        attention_rate.extend(['关注卷用卷率', '-', '-', '-', '-'])
        expire_attention_data.extend(['关注卷失效数', '-', '-', '-', '-'])
        add_promote_data.extend(['新增促活卷数','-', '-', '-', '-'])
        promote_data.extend(['促活卷领卷数','-', '-', '-', '-'])
        used_promote_data.extend(['促活卷用卷数', '-', '-', '-', '-'])
        expire_promote_data.extend(['促活卷失效数', '-', '-', '-', '-'])
        add_neighbor_data.extend(['新增邻店卷数','-', '-', '-', '-'])
        neighbor_data.extend(['邻店卷领卷数','-', '-', '-', '-'])
        used_neighbor_data.extend(['邻店卷用卷数', '-', '-', '-', '-'])
        expire_neighbor_data.extend(['邻店卷失效数', '-', '-', '-', '-'])
        add_basis_data.extend(['新增基础卷数','-', '-', '-', '-'])
        basis_data.extend(['基础卷领卷数','-', '-', '-', '-'])
        used_basis_data.extend(['基础卷用卷数', '-', '-', '-', '-'])
        expire_basis_data.extend(['基础卷失效数', '-', '-', '-', '-'])
        add_scene_data.extend(['新增场景卷数','-', '-', '-', '-'])
        scene_data.extend(['场景卷领卷数','-', '-', '-', '-'])
        used_scene_data.extend(['场景卷用卷数', '-', '-', '-', '-'])
        expire_scene_data.extend(['场景卷失效数', '-', '-', '-', '-'])


        for i in range((end_date - start_date).days):
            x = start_date + datetime.timedelta(i)
            count = 0
            count_used = 0
            count_out_time = 0
            count_downline = 0
            count_modify = 0
            count_expire = 0
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
                    if _sub[5]:
                        count_modify+=1
                    #关注券
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
                    count_attention_rate=count_attention/count_used_attention
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
        df.to_csv(os.path.join(dir_name, 'jhz.csv'), index=False, encoding='gbk', sep=',')
        return all_data


def main():
    export = Export()
    export.jhz('2018-7-5', '2018-7-15', './')


if __name__ == '__main__':
    main()