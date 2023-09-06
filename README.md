Vue+flask_旅游小网站_毕业设计

#### 介绍
毕业设计-flask-vue前后端分离
一款简单的旅游网站，带admin管理系统

#### 软件架构
软件架构说明
使用Python-flask 轻量级框架编写后端程序，前端采用Vue编写，后端接口都在蓝图blueprints中，前端界面后面提供。
![图片](https://github.com/liyixiang545/liyixiang545/assets/94123384/33bda121-9a59-45f2-b4ce-8b41e296106b)

dist文件夹为前端打包的文件，index.html是前端入口
apps/request.py，def_function文件夹为一些构造方法和测试条例
blueprints文件夹里面是一些flask框架蓝图、对每个界面接口进行处理
SqlConfig文件为数据库入口，固定写死了数据库获取端口、用户名、密码等信息 可自行更改
app文件为入口文件，caturemodel文件为验证码模块代码，form文件为处理表单代码，model文件为数据库模型python-orm
requirements.txt 文件为

#### 安装教程

1.  后端代码下载到本地后，环境需要python.3.9.7
2.  使用pycharm工具打开下载的文件夹，安装好部分库，可以使用 pip3 install requirements.txt
3.  安装完成后，pycharm执行启动即可
4.  数据库采用mysql，可以使用phpstuty创建本地数据库，连接的端口为：13306，用户名为：root，密码为：1qazCDE#%TGB，数据库为：lvwz，前期工作做好后
5.  flask拉起来，连接数据库，服务监听5000端口。浏览器网址上输入http://127.0.0.1:5000/_init_new_data，返回OK，则初始化建表完成


#### 演示环境
https://gxfcgss.cf

#### 特技

1.  使用 Readme.md 来支持不同的语言
