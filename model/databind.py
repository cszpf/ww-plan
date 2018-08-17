#encoding=utf-8
import MySQLdb
import os
import pandas as pd
import connectTool
cwd = os.getcwd()

def template(items, ids):
	return {'name':items[1],'id':items[0],'type':ids}


class Connect(connectTool.connect):
    
    # 查询数据库
    def query(self, db_name, sql):
        db = self.connect(db_name)
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        return results

class Databind:
    def __init__(self):
        self.connect = Connect()

    def ADMIN_REGION_CODE(self, data):
        sql = 'SELECT region_code, region_name FROM micro_region WHERE LEVEL=1;'
        result = self.connect.query(self.connect.fenqi, sql)
        return {'ADMIN_REGION_CODE':[template(_,'ADMIN_REGION_CODE') for _ in result]}

    def MICRO_REGION_CODE(self, data):
        sql = "SELECT region_code, region_name FROM micro_region WHERE LEVEL=2 AND parent_region_code='{}';"
        result = self.connect.query(self.connect.fenqi, sql.format(data['opt']['ADMIN_REGION_CODE']))
        return {'MICRO_REGION_CODE':[template(_,'MICRO_REGION_CODE') for _ in result]}

    def MERCHANT_TYPE(self, data):
        sql = "SELECT DISTINCT merchant_type, merchant_type_name FROM merchant_industry;"
        result = self.connect.query(self.connect.fenqi, sql)
        return {'MERCHANT_TYPE':[template(_,'MERCHANT_TYPE') for _ in result]}

    def SALE_NAME(self, data):
        sql = "SELECT DISTINCT sale_name FROM subbranch WHERE sale_name IS NOT NULL;"
        result = self.connect.query(self.connect.fenqi, sql)
        return {'SALE_NAME':[template([i,_[0]],'SALE_NAME') for i, _ in enumerate(result)]}

    def OPERATOR_NAME(self, data):
        sql = "SELECT DISTINCT operator_name FROM subbranch WHERE sale_name IS NOT NULL;"
        result = self.connect.query(self.connect.fenqi, sql)
        return {'OPERATOR_NAME':[template([i,_[0]],'OPERATOR_NAME') for i, _ in enumerate(result)]}

    def MERCHANT_ID(self, data):
        sql = "SELECT merchant_id, merchant_name FROM merchant WHERE merchant_name LIKE '%{}%';"
        result = self.connect.query(self.connect.fenqi, sql.format(data['opt']['MERCHANT_NAME']))
        return {'MERCHANT_ID':[template(_,'MERCHANT_ID') for _ in result]}

    def SUBBRANCH_ID(self, data):
        sql = "SELECT subbranch_id, subbranch_name FROM subbranch WHERE merchant_id='{}';"
        result = self.connect.query(self.connect.fenqi, sql.format(data['opt']['MERCHANT']))
        return {'SUBBRANCH_ID':[template(_,'SUBBRANCH_ID') for _ in result]}

if __name__ == '__main__':
    databind = Databind()
    print(databind.ADMIN_REGION_CODE(''))