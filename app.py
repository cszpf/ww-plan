from flask import Flask, request, render_template, make_response, send_file, jsonify
from flask_cors import CORS
import pickle as pk
import logging
import os
import jinja2
import hashlib
import sys
import datetime
sys.path.append('./model')
from databind import Databind
from util import Export
from util_lz import Export as Export_lz
import pandas as pd
cwd = os.getcwd()
# jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(
#     os.path.join(cwd, 'templates')))
#app = Flask(__name__, static_url_path='',root_path='')
app = Flask(__name__,
            static_folder = 'dataSystem/dist/static',
            template_folder = 'dataSystem/dist')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
_export = Export()
_databind = Databind()
_export_lz = Export_lz()

def write_log():
    app.logger.info('info log')
    app.logger.warning('warning log')

@app.route('/', methods=['GET'])
def signin_form():
    write_log()
    return render_template('index.html')

@app.route('/<path:path>', methods=['GET'])
def x():
    write_log()
    return render_template('index.html')

@app.route('/api/signin', methods=['POST'])
def signin():
    write_log()
    # print(eval(request.data))
    username = eval(request.data).get('username')
    password = eval(request.data).get('password')
    username1 = getMD5(username); password1 = getMD5(password)
    _dict = {
        'username':username,
        'password':password,
        'status':'ok'
        }
    if username1 == '414ccf4cba23f4ed1984caaca8492fff' and password1 == modifyKey(methods='get'):
        pass
    else:
        _dict.update({'status':'账号或密码有误'})
    return jsonify(_dict)

@app.route('/api/pwd', methods=['POST'])
def changePwd():
    data = eval(request.data)
    write_log()
    oldpwd = data.get('oldpwd')
    newpwd = data.get('newpwd')
    twice = data.get('twice')
    _dict = {
        'status':'ok'
        }
    if newpwd != twice:
        _dict.update({'status':'请确认两次输入密码一致'})
        return jsonify(_dict)
    oldpwd = getMD5(oldpwd)
    newpwd = getMD5(newpwd)
    if oldpwd == modifyKey(methods='get'):
        modifyKey(methods='post', object=newpwd)
    else:
        _dict.update({'status':'原密码输入错误'})
    return jsonify(_dict)

@app.route('/api/export', methods=['POST'])
def export():
    data = eval(request.data)
    write_log()
    start_date = data['date'][0]
    end_date = data['date'][1]
    ids = data['ids']
    opt = data.get('opt', {})
    if ids != 'all':
        datas = eval('''_export.{ids}(start_date,end_date,'static',opt)'''.format(ids=ids))
    else:
        datas = all2excel(start_date, end_date)
    data2excel(datas,ids)
    response = make_response(send_file("./static/{ids}.xlsx".format(ids=ids)))
    response.headers['Content-Disposition'] = "attachment;filename={}.xlsx".format(ids)
    return response

@app.route('/api/table_export', methods=['POST'])
def table_export():
    data = eval(request.data)
    write_log()
    start_date = data['date'][0]
    end_date = data['date'][1]
    ids = data['ids']
    opt = data.get('opt', {})
    pages = data.get('page'); cols = data.get('columns')
    pages = 1 if pages * cols == 0 else pages * cols
    if ids in ['mdhz', 'djl']:
    	_cols = [0]
    elif ids in ['qhz']:
    	_cols = list(range(5))
    elif ids in ['mdls', 'mdlszb']:
    	_cols = list(range(10))
    elif ids in ['khhz']:
    	_cols = list(range(6))
    _cols.extend(list(range(pages, pages+cols)))
    if ids not in ['all', 'hymd', 'cmmd', 'ydsh', 'lssh']:
        datas = eval('''_export.{ids}(start_date,end_date,'static',opt)'''.format(ids=ids))[0]
        if ids in ['mdhz']:
            datas = datas[0]
    else:
        if ids in ['all']:
            datas = all2excel(start_date, end_date)[0][0]
        else:
            datas = eval('''_export_lz.{ids}(start_date,end_date,'static',opt)'''.format(ids=ids))
    if ids in ['ydsh', 'lssh', 'hymd', 'cmmd', 'shyq', 'mdpm', 'shqxq', 'qpm']:
    	_cols = list(range(len(datas.columns)))
    return jsonify(datas.iloc[:, _cols].to_dict())

@app.route('/api/databind', methods=['POST'])
def databind():
	data = eval(request.data)
	write_log()
	return jsonify(eval('''_databind.{ids}(data)'''.format(ids=data['id'])))

def data2excel(datas, ids):
    if not os.path.exists('./static'):
        os.makedirs('./static')
    writer = pd.ExcelWriter('./static/{ids}.xlsx'.format(ids=ids))
    try:
        assert len(datas[0]) == len(datas[1])
        for df, i in zip(datas[0], datas[1]):
            if i == '门店汇总':
                df.to_excel(writer, '{i}'.format(i=i), encoding='gbk')
            else:    
                df.to_excel(writer, '{i}'.format(i=i), encoding='gbk', index=False)
    except:
        datas[0].to_excel(writer, '{i}'.format(i=datas[1]), encoding='gbk', index=False)
    finally:
        writer.save()

def all2excel(start_date, end_date):
    main_export = Export()
    datas, mzs = [], []
    for fun in main_export.__dir__():
        if '__' in fun or 'connect' in fun:
            continue
        _datas = eval('''main_export.{}('{}','{}','./static')'''.format(fun,start_date,end_date))
        try:
            assert len(_datas[0]) == len(_datas[1])
            datas.extend(_datas[0]); mzs.extend(_datas[1])
        except:
            datas.append(_datas[0]); mzs.append(_datas[1])
    return datas, mzs

def modifyKey(path='static', **pkgs):
    if not os.path.exists(path):
        os.makedirs(path)
    if pkgs.get('methods') == 'get':
        if not os.path.exists(os.path.join(path,'keys')):
            return 'e10adc3949ba59abbe56e057f20f883e'
        with open(os.path.join(path,'keys'),'rb') as fr:
            return pk.load(fr)
    else:
        with open(os.path.join(path,'keys'),'wb') as fw:
            pk.dump(pkgs['object'], fw)

def getMD5(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode('utf-8'))
    return md5.hexdigest()

if __name__ == '__main__':
    if not os.path.exists('./log'):
        os.makedirs('./log')
    handler = logging.FileHandler('./log/flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port='5000', debug=True)
