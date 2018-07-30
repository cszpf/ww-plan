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
5. install tqdm
  - pip install tqdm

# 文件夹说明
1. sql文件夹下存放的是MySQL数据表的一些索引创建文件
2. static文件夹下存放的是与页面渲染相关的一些js、css包以及地址后缀来源映射规则(rules.txt)
3. templates文件夹下存放的是页面模板，比如登陆页面、导表页面
4. log文件夹下存放的是系统访问日志，用于页面追踪和debug
5. model文件夹下存放的是系统的开发代码：
  - util.py是主程序, 目前主要实现导表功能；
  - connectTool.py为数据库连接工具，主要实现数据库连接功能；
  - click.py是点击量的爬虫代码，主要功能是从指定合作网站中爬取生产系统页面访问信息；

# 部署服务(本地开发不用了解)
1. 需安装flask+uwsgi:在windows安装会出错
  - pip install flask
  - pip install uwsgi
 
2. 在uwsgi中需安装python插件,并新建uwsgi.ini配置文件，需要加入python包的地址
  - sudo apt-get install uwsgi_plugin_python3 
3. 更改数据库连接方式时，只需更改model/connectTool.py文件
4. 另外系统默认采用debug模式，部署到生产环境中时需将debug模式置为False,在app.py的最后一行

# 开发声明
1. 详见之前微信群里发的压缩包中的需求说明文档
主要是仿照./model/util.py的Export类中的第一个函数，按照优先级要求实现其余表的导入导出功能。相应表的导入导出函数用该表的拼音命名。如：导出门店流水是mdls.xlsx

2. 本地运行(debug阶段)
  - python app.py之后，在本地访问127.0.0.1:5000便可访问