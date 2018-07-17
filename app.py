from flask import Flask, request, render_template, make_response, send_file
import logging
import os
import jinja2
import hashlib
import sys
import datetime
sys.path.append('./model')
from util import Export
cwd = os.getcwd()
jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(
    os.path.join(cwd, 'templates')))
app = Flask(__name__, static_url_path='',root_path='')
_export = Export()

@app.route('/', methods=['GET'])
def signin_form():
    app.logger.info('info log')
    app.logger.warning('warning log')
    return render_template('sign-form.html')

@app.route('/signin', methods=['POST'])
def signin():
    app.logger.info('info log')
    app.logger.warning('warning log')
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
    app.logger.info('info log')
    app.logger.warning('warning log')
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    ids = request.form['ids']
    if start_date == '' or end_date == '' or start_date > end_date or datetime.datetime.strptime(end_date, '%Y-%m-%d').date()>datetime.date.today():
        return render_template('table-export.html', start_date=start_date, end_date=end_date)
    eval('''_export.{ids}(start_date,end_date,'./static')'''.format(ids=ids))
    response = make_response(send_file("./static/{ids}.csv".format(ids=ids)))
    response.headers['Content-Disposition'] = "attachment;filename={}.csv".format(ids)
    return response

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
    