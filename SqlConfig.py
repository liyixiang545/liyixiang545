# from sqlalchemy import create_engine
from sqlalchemy import create_engine

# 数库的配置文件
HOST = 'localhost'
PORT = 3306
USERNAME = 'root'
PASSWORD = '1qazCDE#5tgb'
DB = 'lywz'
# dialect + driver://username:passwor@host:port/database
DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'
# DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'.format(USERNAME,PASSWORD,HOSTANAME,PORT,DATABASE)
# DB_URI = 'mysql+pymysql://root:123456@localhost:3306/lywz'
# engine = create_engine(DB_URI,echo=False,pool_size=10)  # 创建引擎
# conn = engine.connect()  # 连接

# 配置数据库
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_TIMEOUT = 3600
SQLALCHEMY_POOL_RECYCLE = 3600
# 配置数据库密钥
SECRET_KEY = "1qazCDE#5tgb"

engine = create_engine(DB_URI, echo=False, pool_size=100)

conn = engine.connect()  # 连接
def mysql_init_conn():
    return conn




# engine = create_engine(DB_URI,echo=False,pool_size=10)  # 创建引擎
# conn = engine.connect()  # 连接


# 在app配置用这个方式
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SECRET_KEY'] = "123456"

