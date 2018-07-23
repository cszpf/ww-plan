from flask import Flask, request, render_template, make_response, send_file
import logging
import os
import jinja2
import hashlib
import sys
import datetime
sys.path.append('./model')
from util import Export
import pandas as pd

cwd = os.getcwd()
jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(
    os.path.join(cwd, 'templates')))
app = Flask(__name__, static_url_path='',root_path='')
_export = Export()

def write_log():
    app.logger.info('info log')
    app.logger.warning('warning log')

@app.route('/', methods=['GET'])
def signin_form():
    write_log()
    return render_template('sign-form.html')

@app.route('/signin', methods=['GET'])
def x():
    return render_template('sign-form.html')

@app.route('/export', methods=['GET'])
def x1():
    return render_template('sign-form.html')

@app.route('/signin', methods=['POST'])
def signin():
    write_log()
    md5 = hashlib.md5()
    username = request.form['username']
    password = request.form['password']
    md5.update(username.encode(encoding='utf-8'))
    username1 = md5.hexdigest()
    md5 = hashlib.md5()
    md5.update(password.encode(encoding='utf-8'))
    password1 = md5.hexdigest()
    if username1 == '414ccf4cba23f4ed1984caaca8492fff' and password1 == 'e10adc3949ba59abbe56e057f20f883e':
        return render_template('table-export.html')
    return render_template('sign-form.html', message='admin or password error', username=username)

@app.route('/export', methods=['POST'])
def export():
    write_log()
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    ids = request.form['ids']
    if start_date == '' or end_date == '' or start_date > end_date or datetime.datetime.strptime(end_date, '%Y-%m-%d').date()>(datetime.date.today()+datetime.timedelta(1)):
        return render_template('table-export.html', start_date=start_date, end_date=end_date)
    if ids != 'all':
        datas = eval('''_export.{ids}(start_date,end_date,'./static')'''.format(ids=ids))
    else:
        datas = all2excel(start_date, end_date)
    data2excel(datas,ids)
    response = make_response(send_file("./static/{ids}.xlsx".format(ids=ids)))
    response.headers['Content-Disposition'] = "attachment;filename={}.xlsx".format(ids)
    return response

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
    
