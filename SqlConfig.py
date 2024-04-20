from sqlalchemy import create_engine
from configparser import ConfigParser
import redis
from def_function.uplogger import loggerInfo,loggerError,loggerWarning
import time

def get_time():
    T = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return T

# 数据库的配置文件
# 配置文件
cf = ConfigParser()
cf.read('.env')

# 获取配置文件数据库登录用户名
HOST = cf.get('mysql', 'host')
# HOSTNAME = '127.0.0.1'
PORT = cf.get('mysql', 'port')
# PORT = '3306'
USERNAME = cf.get('mysql', 'user')
PASSWORD = cf.get('mysql', 'password')
# DB = 'root'
database = cf.get('mysql', 'database')
# dialect + driver://username:passwor@host:port/database
DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{database}'
# DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'.format(USERNAME,PASSWORD,HOSTANAME,PORT,DATABASE)


# 获取配置文件redis登录用户名
redis_HOST = cf.get('redis', 'host')
# HOSTNAME = '127.0.0.1'
redis_PORT = cf.get('redis', 'port')
# PORT = '3306'
redis_PASSWORD = cf.get('redis', 'password')
# DB = 'root'
redis_db = cf.get('redis', 'db')
# 配置数据库
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI =DB_URI
# 配置数据库密钥
SECRET_KEY = "1qazCDE#5tgb"

engine = create_engine(DB_URI, pool_size =100, max_overflow = 50, pool_timeout = 200)  # 创建引擎

# redis使用 缓存池
pool = redis.ConnectionPool(host=redis_HOST, port=redis_PORT, password=redis_PASSWORD,decode_responses=True,max_connections=20)

def redis_pool():
    r = redis.Redis(connection_pool=pool)
    return r


Count = 0
def Conn():
    global Count
    try:
        Count = Count + 1
        print(f"正在建立{HOST}:{PORT}:{database}数据库的连接")
        db_conn = engine.connect()  # 连接
        print("数据库连接成功")
        return db_conn
    except Exception as e:
        print("数据库链接异常，请检查数据库配置情况！")
        loggerError(get_time() + ' ' + ' ' + ' ' + str(e))
        time.sleep(3)
        if Count < 4:
            print("尝试第{0}次重新链接！".format(Count))
            Conn()
        else:
            print("系统连续{0}次连接数据库失败，请查看数据库配置情况".format(Count-1))

def close_conn(conn):
    if conn:
        conn.close()









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
