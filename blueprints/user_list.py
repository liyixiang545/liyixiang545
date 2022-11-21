from flask import (Blueprint,
                   render_template,
                   request,
                   session,
                   redirect,
                   url_for,
                   jsonify,
                   flash,
                   make_response,
                   g,
                   )
from utils import CaptchaTool
from form import LoginForm, RigisterForm
from exts import db
from model import CatureModel, UserModel
import redis
import json
import time
from werkzeug.security import generate_password_hash, check_password_hash
# redis使用 缓存池
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
bp = Blueprint("user", __name__, url_prefix="/User")
from exts import mysql_init_conn


# 获取验证码
@bp.route('/GetCaptcha', methods=["GET"])
def get_captcha():
    """
    获取图形验证码
    :return:
    """
    mysql_init_conn()
    new_captcha = CaptchaTool()
    # 获取图形验证码
    img, code = new_captcha.get_verify_code()
    # 存入session
    session["code"] = code
    # 存入redis缓存中
    r.setex("code", 65, code)
    # print("最新验证码：", code)
    # print("5s后redis：",r.get('code'))  # 5秒后，取值就从orange变成None
    # code_hash = generate_password_hash(code)

    # ca_sql = """insert into cature (id,cature_code,cature_hash) values (%s,%s,%s)"""
    # values = (int(),int(code),(img))
    # cursor.execute(ca_sql, values)

    cature = CatureModel(cature_code=code, cature_hash=img)
    db.session.add(cature)
    db.session.commit()
    # js_img = str(img)
    mysql_init_conn().close()
    # cursor.close()
    # conn.close()
    return img
    # return code

# @bp.route('/testVerifyCaptcha', methods=["POST"])
# def test_verify_captcha():
#     """
#     验证图形验证码
#     :return:
#     """
#     #obj = request.get_json(force=True)
#     #obj = request.args.get('code')##作为查询字符串:/book?id=1 把值传回后端
#     obj = request.get_json()
#     # 获取用户输入的验证码
#     code = obj.get("code",None)
#     # 获取session中的验证码
#     #s_code = session.get("code", None)
#     print(code)
#     # if not all([code, s_code]):
#     #     return "参数错误"
#     # if code != s_code:
#     #     return "验证码错误"
#     return "验证成功"

# 请求来了 对请求前处理
# 请求来之前
@bp.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        try:
            user = UserModel.query.get(user_id)

            # print(user.username)
            # 给g绑定一个user变量的值
            # setattr(g,"user",user)
            # 全局变量g
            g.user = user
            # print(g.user.username)

        except:
            # g.user = None
            pass
    else:
        pass

# 请求来了->before_request->视图函数->视图函数中返回模板->context_processor

# 上下文处理器 渲染所有模板都会执行这个
# @bp.context_processor
# def context_processor():
#     if hasattr(g,"user"):
#         print(g)
#         return {"user":g.user}
#     else:
#         return {}


@bp.route("/Logout")
def logout():
    # 清除session 所有数据
    time.sleep(1)
    session.clear()
    return jsonify({"code": 200, "msg": "退出成功", "data": ""})



# 处理登录模块
# 普通界面 正常传值到后端进行处理
# 登录接口
@bp.route('/Login', methods=['POST'])
def login():
    # if request.method == 'GET':
    #     return render_template("login.html")
    # else:
    mysql_init_conn()
    cc = request.get_data()  # 获取请求过来的数据request.data
    data = json.loads(cc)  # request.get_data(as_text=True) ：获取前端POST请求传过来的 json 数据,将已编码的 JSON 字符串解码为 Python 对象
    # data1 = json.dumps(data, indent=4)  # 将data转换为json格式复制给data1  ，将python对象编码为json字符串
    # print(data['email'])#输出对象内的email值
    # print(data['password'])
    email = data['email']
    password = data['password']
    # print(email, password)
    if email == '' and password == '':  # 后端判断邮箱和密码是否为空
        # time.sleep(1)
        return jsonify({"code": 201, "msg": '账号或者密码为空!'})
    else:
        if email == 'admin@qq.com':
            user = UserModel.query.filter_by(email=email).first()
            # sql = "SELECT * FROM USER WHERE EMAIL='admin@qq.com'"
            # conn.execute(sql)
            password = data['password']
            try:
                if check_password_hash(user.password, password) and user:
                    session["user_id"] = user.id  # 设置session
                    # time.sleep(0.5)
                    mysql_init_conn().close()
                    return jsonify({'code': 201, 'msg': "admin登录", "user": user.username})
                else:
                    mysql_init_conn().close()
                    return jsonify({"code": 400, "msg": "邮箱和密码不匹配！请仔细检查!"})
            except:

                pass

        else:
            user = UserModel.query.filter_by(email=email).first()  # 判断邮箱 查询数据库 email 是否和传入的email相同或者是否存在账户
            if user:
                session["user_id"] = user.id  # 设置session
                if user.status == 0:
                    mysql_init_conn().close()
                    time.sleep(1)
                    return jsonify({"code": 405, "msg": '邮箱已被管理员注销，若需要登录，请联系管理员！'})
                else:
                    if check_password_hash(user.password, password):
                        # user 目前是数据库的数据
                        mysql_init_conn().close()
                        return jsonify({"code": 200, "msg": '普通用户登录成功!', "user": user.username})  # 跳转回首页
                    else:
                        # flash("邮箱和密码不匹配！请仔细检查")
                        mysql_init_conn().close()
                        time.sleep(1)
                        return jsonify({"code": 400, "msg": "邮箱和密码不匹配！请仔细检查!"})
            else:
                mysql_init_conn().close()
                return jsonify({"code": 401, "msg": "邮箱不存在"})


# 个人登录信息模块 前端传后端 怎样的url信息 后端怎么去处理和找到该信息
@bp.route('/Profile')
def profile():
    # 作为url组成部分:/Profile/1
    # 作为查询字符串:/Profile?id=1
    user_id = request.args.get('id')  # 收到传回的id值并返回那个界面 获取参数 args.get('id')
    # print(user_id)
    if user_id:
        return '用户个人中心'
    else:
        return redirect(url_for("user.rigister"))  # url_for指定里面是路径下的方法名


@bp.route('/Admin', methods=['GET'])
def admin():
    if hasattr(g, 'user'):
        # print(g.user.username)
        if g.user.username == 'admin':
            return jsonify({"code": 200, "msg": "存在登录可以跳转", "status": 1})
        else:
            return jsonify({"code": 400, "msg": "未登录admin", "status": 2})
    else:
        session.clear()
        return jsonify({"code": 400, "msg": "未登录admin", "status": 2})
# T4 = myThread(5,'admin线程',1,admin,5)
# T4.start()


# #登录jinja2表单处理
# @bp.route('/Login',methods=['POST','GET'])
# def login():
#     #解决跨域请求问题
#     if request.method == 'GET':
#         #return  render_template("login.html")
#         return render_template("login.html")
#     else:
#
#         form = LoginForm(request.form)  # 处理登录模块，若是post请求则去做表单验证
#         email = form.email.data
#         password = form.password.data
#         print(email,password)
#         if email == '' and password =='':#
#             return jsonify({"code": 200, "msg": '账号或者密码为空!'})
#         else:
#             # 这个⽅法是实现表单校验功能的 csrf，数据正确性 都通过了 则为真 否则为假
#             if form.validate():#判断表单是否为真值(验证正确) 用validate
#                 # print(form.email.data)  # 取出email⾥⾯的value值
#                 # print(form.password.data)
#                 email = form.email.data
#                 password = form.password.data
#                 user = UserModel.query.filter_by(email=email).first()
#                 if user and check_password_hash(user.password,password):
#                     session["user_id"] = user.id
#                     print("登录成功")
#                     return jsonify({"code": 200, "msg": '登录成功!'}) #跳转回首页
#                 else:
#                     flash("邮箱和密码不匹配！请仔细检查")
#                     return redirect(url_for("user.login"))
#             else:
#                 return jsonify({"code": 200, "msg": "邮箱或者密码输入错误"})

# 获取邮箱验证码
# @bp.route("/Mail", methods=['POST', 'GET'])
# def my_mail():
#     message = Message(
#         subject="邮箱测试",
#         recipients=['737709449@qq.com'],
#         # 收件人
#         body="您的验证码为:",
#         # 邮箱内容
#
#     )
#     mail.send(message)
#     return "wufa"


# 传值 json
# @bp.route("/Rigister",methods=['POST',"GET"])
# def rigister():
#     try:
#         if request.method == 'GET':
#             return render_template("rigisterceshi.html")
#         else:
#             cc = request.get_data()#获取请求过来的数据
#
#             #print(cc)#打印 数据
#             data = json.loads(cc)  # request.get_data(as_text=True) ：获取前端POST请求传过来的 json 数据,将已编码的 JSON 字符串解码为 Python 对象
#             data1 = json.dumps(data,indent=4)# 将data转换为json格式复制给data1  ，将python对象编码为json字符串
#             #print(data['email'])#输出对象内的email值
#             print(data1)#输出已经成为json格式的数据 json格式
#
#             password = data['password']
#             pwdcfm = data['pwdcomfirm']
#             user = data['user']
#             cature = data['cature']
#             email = data['email']
#
#             print("用户名为：",user)  # 取出user⾥⾯的value值
#             print("密码为：",password)  # 取出password⾥⾯的value值
#             print("确认密码为：", pwdcfm)  # 拿到email的整个标签
#             print("邮箱为：",email)  # 取出email⾥⾯的value值
#             print("验证码为：", cature)  # ⾥⾯的value值
#             hash_pwdcfm = generate_password_hash(pwdcfm)
#
#             #判断验证码和redis缓存中是否一致
#             if r.get("code") == cature:
#                 #if password == pwdcfm:
#                 email= data['email']
#                 print(email)
#                 if UserModel.query(user).filter_by(email=email).first():# 遍历数据库
#                     print(UserModel.query.filter_by(email=email).first())
#                     user = UserModel(username=user,password=hash_pwdcfm,email=email)
#                     db.session.add(user)
#                     db.session.commit()
#                     print("redis验证码为：",r.get('code'))  # 5秒后，取值就从orange变成None
#                     return jsonify({"code" : 200,"msg":'注册成功'})
#                 else:
#                     print(UserModel.query.filter_by(email=email).first())
#                     return jsonify({"code": 402,"msg": "邮箱已注册!"})
#             # else:
#             #     # redirect(url_for("user.login"))
#             #     print(cature)
#             #     print(r.get("code"))
#             #     return jsonify({"code": 400,"msg": "两次密码输入不一致!"})
#             else:
#                 return jsonify({"code":401,"msg":"验证码错误"})
#     except:
#         return jsonify({"code":500,"msg":"接口异常!"})

# 处理注册模块 jinja2使用正常 前端传回的json数据或者表单数据不能识别

# 注册接口
@bp.route('/Rigister', methods=['POST', 'GET'])
def rigister():
    mysql_init_conn()
    if request.method == 'GET':
        # return render_template("rigisterceshi.html", **content, form=rigiter_form)  # 模板渲染,传入关键字参数值模板
        pass
    else:
        form = RigisterForm(request.form)
        # 处理登录模块，若是post请求则去做表单验证
        if form.validate():  # 判断表单是否为真值(验证正确) 用validate
            # 拿到前端传回来的值 并赋值到变量对象中
            user = form.user.data
            pwdcfm = form.pwdcomfirm.data
            email = form.email.data
            codedata = form.cature.data
            # 对获取到的密码进行hash加密(python内部的加密,非md5)
            hash_pwdcfm = generate_password_hash(pwdcfm)
            createtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            updatatime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 判断验证码和redis缓存中是否一致
            if r.get("code") == codedata:
                emailcomfirm = UserModel.query.filter_by(email=email).first()
                if email == emailcomfirm:
                    if emailcomfirm.status == 0:
                        mysql_init_conn().close()
                        time.sleep(1)
                        return jsonify({"code": 405, "msg": '邮箱已被管理员注销，若需要登录，请联系管理员！'})
                    else:
                        mysql_init_conn().close()
                        time.sleep(1)
                        return jsonify({"code": 402, "msg": '邮箱存在，请重新注册！'})
                else:
                    user = UserModel(username=user, password=hash_pwdcfm, email=email, create_time=createtime,
                                     updata_time=updatatime, status='1',img="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png")
                    db.session.add(user)
                    db.session.commit()
                    # print("redis验证码为：", r.get('code'))  # 5秒后，取值就从orange变成None
                    mysql_init_conn().close()
                    time.sleep(1)
                    return jsonify({"code": 200, "msg": '注册成功'})
                    pass
            else:
                mysql_init_conn().close()
                time.sleep(1)
                return jsonify({"code": 401, "msg": "验证码错误，请重新输入!"})
        else:
            mysql_init_conn().close()
            return jsonify({"code": 400, "msg": "验证失败，邮箱已存在或格式有误，请重新输入！", "status": "1"})
    # except:
    #     # print("注册接口异常，清仔细检查！")
    #     return jsonify({"code": 500, "msg": "注册接口异常，清仔细检查！", "status": "10"})
# T4 = myThread(6,'注册threard',1,rigister,5)
# T4.start()
# 查询数据表用户
@bp.route('/GetUser_List', methods=['GET'])
def getuser_list():
    mysql_init_conn()
    user_list = []
    # 定义为列表
    try:
        # 查询该数据库长度(条数)
        count = UserModel.query.count()
        # print(count)
        for i in range(count):
            list = UserModel.query.filter_by(id=i+1).all()[0]
            # [0]列表 代表取第一个值
            # UserModel.query.filter_by(id=i).all() 返回的是[<UserModel 1>]这是一个列表 UserModel.query.filter_by(id=i).all()[0]取第一个值
            # print(list)
            if list.id != '':
                if list.status == 1:
                    user_list.append({"email": list.email, "username": list.username, "create_time": list.create_time,
                                      "updata_time": list.updata_time, "status": list.status, "id": list.id})

                    time.sleep(1)
                # print(i)
                else:

                    pass
            else:
                i = list.id

                pass
            # append 列表添加{}大括号 json数据 把多个字典变成列表
    except:

        pass
    mysql_init_conn().close()
    time.sleep(0.5)
    return jsonify(user_list)
# T5 = myThread(7,'用户thread',10,getuser_list,5)
# T5.start()
# 获取被删除用户列表接口
@bp.route('/GetUserDelete_List', methods=['GET'])
def getuserdetele_list():
    mysql_init_conn()
    userdetele_list = []
    # 定义为列表
    try:
        # 查询该数据库长度(条数)
        count = UserModel.query.count()
        # print(count)
        for i in range(count):
            list = UserModel.query.filter_by(id=i+1).all()[0]

            # print(i)
            # [0]列表 代表取第一个值
            # UserModel.query.filter_by(id=i).all() 返回的是[<UserModel 1>]这是一个列表 UserModel.query.filter_by(id=i).all()[0]取第一个值
            # print(list)
            if list.id != '':
                if list.status == 0:
                    userdetele_list.append({"email": list.email, "username": list.username, "create_time": list.create_time,
                                      "updata_time": list.updata_time, "status": list.status, "id": list.id})
                # print(i)
                else:

                    pass
            else:
                i = list.id

                pass
            # append 列表添加{}大括号 json数据 把多个字典变成列表
    except:

        pass
    mysql_init_conn().close()
    time.sleep(0.5)
    return jsonify(userdetele_list)

# 删除账户(假状态删除)
@bp.route('/DeleteUser_List', methods=['POST','PUT'])
def deleteuser_list():
    mysql_init_conn()
    da = request.get_data()
    # print(da)
    data = json.loads(da)  # json.loads 把传回来的值整成字典
    # print(data['email'])
    # 获取字典里面的key为email的值
    # 传回来的data 获取字典里面的msg的值
    emailexec = data['msg']
    up_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 修改数据 删除账户把账户状态值设为0、更新时间
    emailcache = UserModel.query.filter_by(email=emailexec)[0]
    emailcache.status = 0
    emailcache.updata_time = up_time
    db.session.commit()
    time.sleep(0.5)
    mysql_init_conn().close()
    return jsonify({"code":200,"msg":"删除成功","status":1})

# 恢复账户
@bp.route('/RecoverUser_List', methods=['POST','PUT'])
def RecoverUser_List():
    mysql_init_conn()
    da = request.get_data()
    # print(da)
    data = json.loads(da)  # json.loads 把传回来的值整成字典
    # print(data['email'])
    # 获取字典里面的key为email的值
    # 传回来的data 获取字典里面的msg的值
    emailexec = data['msg']
    up_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 修改数据 删除账户把账户状态值设为0
    emailcache = UserModel.query.filter_by(email=emailexec)[0]
    emailcache.status = 1
    emailcache.updata_time = up_time
    db.session.commit()
    mysql_init_conn().close()
    time.sleep(0.5)
    return jsonify({"code": 200,"msg":"恢复成功","status":1})


@bp.route('/changepasswd', methods=['POST','PUT'])
def changepasswd():
    mysql_init_conn()
    da = request.get_data()
    data = json.loads(da)  # json.loads 把传回来的值整成字典
    # 获取字典里面的key为email的值
    # 传回来的data 获取字典里面的oldpwd的值
    emailuser = data['user']
    emailpwd = data['oldpwd']
    cfpwd = data['cfpwd']
    nowpwd = data['nowpwd']
    up_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 修改密码、更新时间
    if cfpwd == nowpwd:
        if len(nowpwd) >= 6:
            emailcache = UserModel.query.filter_by(email=emailuser)[0]
            if check_password_hash(emailcache.password, emailpwd):
                hash_nowpwd = generate_password_hash(nowpwd)
                # hash加密
                emailcache.password = hash_nowpwd
                # 加个更新时间
                emailcache.updata_time = up_time
                db.session.commit()

                time.sleep(0.5)
                mysql_init_conn().close()
                return jsonify({"code": 200, "msg": "密码修改成功", "status": 1})
            else:

                time.sleep(0.5)
                mysql_init_conn().close()
                return jsonify({"code": 400, "msg": "密码输入错误，请重新输入", "status": 0})
        else:

            time.sleep(0.5)
            mysql_init_conn().close()
            return jsonify({"code": 400, "msg": "密码至少6位，请重新输入", "status": 0})
    else:
        mysql_init_conn().close()
        return jsonify({"code": 400, "msg": "两者密码不同，请重新修改", "status": 1})

