from SqlConfig import mysql_init_conn
# import pymysql
from apps import create_db,create_migrate,create_mail

# conn = pymysql.connect(host="localhost",
#                    user="root",
#                    password="123456",
#                     db="lywz",
#                     port=3306,
#                     max_allowed_packet=10000,
#                     charset="utf8")
# cursor = conn.cursor()

db = create_db()
migrate = create_migrate()
mail =create_mail()

mysql_init_conn()
#
# def get_pymysql_conn():
#     return conn ,cursor

# i = 0
# while 1:
#     i = i+1
#     print("执行了{}次".format(i))
#     get_pymysql_conn()
# try:
#     i = 0
#     while 1:
#         i = i+1
#         print("执行了{}次".format(i))
#         get_pymysql_conn1()
# except:
#     pass

