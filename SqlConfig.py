from sqlalchemy import create_engine
import pymysql
# 数据库的配置文件
HOST = 'localhost'
# HOSTNAME = '127.0.0.1'
PORT = 3306
# PORT = '3306'
USERNAME = 'root'
PASSWORD = '123456'
# DB = 'root'
database = 'lywz'
# dialect + driver://username:passwor@host:port/database
DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{database}'
# DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'.format(USERNAME,PASSWORD,HOSTANAME,PORT,DATABASE)

# 配置数据库
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI =DB_URI
# 配置数据库密钥
SECRET_KEY = "1qaz@WSX#EDC"

engine = create_engine(DB_URI, pool_size =100, max_overflow = 50, pool_timeout = 20)  # 创建引擎


def Conn():
    conn = engine.connect()  # 连接
    # print("建立数据库链接")
    return conn







# 在app配置用这个方式
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SECRET_KEY'] = "123456"


# 邮箱配置文件
# 当前使用的是QQ邮箱
# MAIL_SERVER = "smtp.qq.com"
# MAIL_PORT = 465
# MAIL_USE_TLS = False
# MAIL_USE_SSL = True
# MAIL_DEBUG = True
# MAIL_USERNAME = "1370586826@qq.com"
# MAIL_PASSWORD = "keaihhmmpspojigf"
# MAIL_DEFAULT_SENDER = "1370586826@qq.com"
# MAIL_MAX_EMAILS =
# MAIL_SUPPRESS_SEND =
# MAIL_ASCII_ATTACHMENTS =
