Vue+flask_旅游小网站_毕业设计

#### 介绍
毕业设计-flask-vue前后端分离
一款简单的旅游网站，带admin管理系统

#### 软件架构
软件架构说明
使用Python-flask 轻量级框架编写后端程序，前端采用Vue编写，后端接口都在蓝图blueprints中，前端界面后面提供。
![图片](https://github.com/liyixiang545/liyixiang545/assets/94123384/a37f0d27-e534-4e49-9283-21e91933c531)

dist文件夹为前端打包的文件，index.html是前端入口

apps/request.py，def_function文件夹为一些构造方法和测试条例

blueprints文件夹里面是一些flask框架蓝图、对每个界面接口进行处理

SqlConfig文件为数据库入口，固定写死了数据库获取端口、用户名、密码等信息 可自行更改

app文件为入口文件，caturemodel文件为验证码模块代码，form文件为处理表单代码，model文件为数据库模型python-orm

requirements.txt 文件为python库文件  需要执行pip3 install requirements.txt安装库

#### 安装教程

1.  后端代码下载到本地后，环境需要python.3.9.7
2.  使用pycharm工具打开下载的文件夹，安装好部分库，可以使用 pip3 install requirements.txt
3.  安装完成后，pycharm执行启动即可
4.  数据库采用mysql，可以使用phpstuty创建本地数据库，连接的端口为：13306，用户名为：root，密码为：1qazCDE#%TGB，数据库为：lvwz，前期工作做好后
5.  flask拉起来，连接数据库，服务监听5000端口。浏览器网址上输入http://127.0.0.1:5000/_init_new_data，返回OK，则初始化建表完成

#### 项目部署

Linux

    git clone https://gitee.com/liyixiang545/vue_flask_bata.git
    cd vue_flask_bata
    python -m venv venv #创建python虚拟环境
    source venv/bin/activate
    pip install -r requirements.txt # 安装项目依赖，可能不全，根据提示自行安装即可
    export FLASK_ENV=development
    vi env # 修改数据库、redis等相关信息
    flask run # 启动 或者 python app.py
    flask 拉起来，连接数据库，服务监听5000端口。浏览器网址上输入 http://127.0.0.1:5000/_init_new_data ，返回OK，则初始化建表完成。
    若部署在服务器，前端代码打包在dist目录下，把对应前端代码目录在nginx配置文件进行部署，则需要修改nginx.conf
    
![图片](https://github.com/liyixiang545/liyixiang545/assets/94123384/ee27ca85-3154-4ad5-837e-5d1b7e6c8521)



Windows

    git clone https://gitee.com/liyixiang545/vue_flask_bata.git
    cd vue_flask_batavue_flask_bata
    python -m venv venv #创建python虚拟环境
    .\venv\Scripts\activate.bat #激活虚拟环境
    pip install -r requirements.txt # 安装项目依赖，可能不全，根据提示自行安装即可
    set FLASK_ENV=development
    vi env # 修改数据库、redis等相关信息
    flask run # 启动 或者 python app.py
    flask 拉起来，连接数据库，服务监听5000端口。浏览器网址上输入 http://127.0.0.1:5000/_init_new_data ，返回OK，则初始化建表完成。
    若部署在windows服务器，前端代码打包在dist目录下，把对应前端代码目录在nginx配置文件进行部署，则需要修改nginx.conf


#### 演示环境
https://gxfcgss.cf

#### 特技

1.  使用 Readme.md 来支持不同的语言
