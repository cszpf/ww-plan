# 依赖及运行环境
1. 运行环境为Python3.X
2. 需安装mysqlclient
  - For Ubuntu
  - sudo apt-get install libmysql-dev
  - sudo apt-get install libmysqlclient-dev
  - sudo apt-get install python-dev
  - sudo pip install mysqlclient
  - For Windows
  - pip install mysqlclient 
3. install openpyxl
  - pip install openpyxl
4. install pandas
  - pip install pandas

# 部署服务(本地开发不用了解)
1. 需安装flask+uwsgi:在windows安装会出错
  - pip install flask
  - pip install uwsgi
 
2. 在uwsgi中需安装python插件,并新建uwsgi.ini配置文件，需要加入python包的地址
  - sudo apt-get install uwsgi_plugin_python3 

# 开发声明
1. 详见之前微信群里发的压缩包中的需求说明文档
主要是仿照./model/util.py的Export类中的第一个函数，按照优先级要求实现其余表的导入导出功能。相应表的导入导出函数用该表的拼音命名。如：导出门店流水是mdls.xlsx

2. 本地运行 
  - python app.py之后，在本地访问127.0.0.1:5000便可访问