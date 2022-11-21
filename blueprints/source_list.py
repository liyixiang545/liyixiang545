from flask import (Blueprint,
                   request,
                   # session,
                   # redirect,
                   jsonify,
                   # g,
                   json,

                   )
import time
# import requests
# import re
# import base64
from form import UpsourceForm
from model import SourceModel
from exts import db,mysql_init_conn
from threading import Thread
bp = Blueprint('source', __name__, url_prefix="/source")
# conn = mysql_conn()
@bp.route('/addSource', methods=['POST','PUT'])
def post_addSource():
    mysql_init_conn()
    if request.method == 'GET':
        pass
    else:
        form = UpsourceForm(request.form)
        if form.validate():
            imgurl = form.img.data
            msg = form.msg.data
            title = form.title.data
            name = form.name.data
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            image_path = './static/img/' + name
            url = 'http://127.0.0.1:5000/static/img/' + name
            imgurl1 = imgurl.encode()
            # with open(image_path, 'wb+') as f:
            #     f.write(imgurl1)
            #     f.close()
            with open(image_path, 'wb') as f:
                f.write(imgurl1)
            f.close()
            # url1 = 'http://127.0.0.1:5000/static/img/' + name
            # data = requests.get(imgurl1).content
            # print(data)
            # with open('./static/img/some.txt', 'wb') as f:
            #     f.write(b'hello world ')
            # f.close()
            # print(f)
            # img = request.files.get(imgurl)
            print(imgurl)
            print(type(imgurl))
            print(type(imgurl1))
            print(imgurl1)
            print(url)
            # img1 = requests.get(imgurl)
            # img2 = requests.get(url)

            # blobimg = img.content
            # print(type(blobimg))
            # print(blobimg)
            # print(blobimg2)
            # print(type(blobimg2))
            # ds.write(blobimg2)
            # ds.write(blobimg)

            # try:
            # for line in imgurl:
            # # re.match, 从开头匹配字符串，如果匹配到返回匹配到的对象。没有匹配到返回None。
            # r = re.match("http", line)
            # print(r)
            # if r == None:
            if imgurl != '':
                Source = SourceModel(source_msg=msg, source_title=title, source_img=url, status=1,
                                     create_time=create_time, update_time=create_time)
                db.session.add(Source)
                db.session.commit()
                mysql_init_conn().close()
            else:
                mysql_init_conn().close()
                return jsonify({"code": 400,"msg":"照片上传失败，请刷新后重新上传","status":1})
            mysql_init_conn().close()
            return jsonify({"code": 200, "msg": "上传成功", "status": 1})
        # except:
            #     return jsonify({"code": 400,"msg":"上传图片异常","status":1})
        else:
            time.sleep(0.5)
            mysql_init_conn().close()
            return jsonify({"code": 400, "msg": "上传验证失败", "status": 1})



@bp.route('/DeleteSource', methods=['POST'])
def post_DeleteSource():
    mysql_init_conn()
    da = request.get_data()
    # print(da)
    data = json.loads(da)  # json.loads 把传回来的值整成字典
    # sourceuser = data['user']
    sourcemsg = data['msg']
    up_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 修改数据 删除账户把账户状态值设为0
    sourcecache = SourceModel.query.filter_by(source_msg=sourcemsg)[0]
    sourcecache.status = 0
    sourcecache.updata_time = up_time
    db.session.commit()
    time.sleep(0.5)
    mysql_init_conn().close()
    return jsonify({"code": 200, "msg": "删除成功", "status": 1})

@bp.route('/RecoverSource', methods=['POST'])
def post_RecoverSource():
    mysql_init_conn()
    da = request.get_data()
    # print(da)
    data = json.loads(da)  # json.loads 把传回来的值整成字典
    # sourceuser = data['user']
    sourcemsg = data['msg']
    up_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 修改数据 删除账户把账户状态值设为0
    sourcecache = SourceModel.query.filter_by(source_msg=sourcemsg)[0]
    sourcecache.status = 1
    sourcecache.updata_time = up_time
    db.session.commit()
    mysql_init_conn().close()
    time.sleep(0.5)
    return jsonify({"code": 200, "msg": "删除成功", "status": 1})

@bp.route('/tourist_resources', methods=['Get'])
def get_tourist_sources():
    mysql_init_conn()
    tourist_list = []
    # sourceuser = data['user']
    # 定义为列表
    # try:
    # 查询该数据库长度(条数)
    count = SourceModel.query.count()
    # print(count)
    for i in range(0, count):
        list = SourceModel.query.filter_by(id=i + 1).all()[0]
        # [0]列表 代表取第一个值
        # UserModel.query.filter_by(id=i).all() 返回的是[<UserModel 1>]这是一个列表 UserModel.query.filter_by(id=i).all()[0]取第一个值
        # print(list)
        if list.id != '':
            if list.status == 1:
                tourist_list.append(
                    {"title": list.source_title, "msg": list.source_msg, "img": list.source_img, "status": list.status})
            else:
                mysql_init_conn().close()
                pass
        else:
            i = list.id
            mysql_init_conn().close()
            pass
        # append 列表添加{}大括号 json数据 把多个字典变成列表

    # except:
    #     print("获取资源异常")
    mysql_init_conn().close()
    time.sleep(0.5)
    return jsonify(tourist_list)



@bp.route('/Delete_tourist_resources', methods=['Get'])
def get_Delete_tourist_sources():
    mysql_init_conn()
    Delete_tourist_list = []
    # 定义为列表
    try:
    # 查询该数据库长度(条数)
        count = SourceModel.query.count()
        # print(count)
        for i in range(0, count):
            list = SourceModel.query.filter_by(id=i + 1).all()[0]
            # [0]列表 代表取第一个值
            # UserModel.query.filter_by(id=i).all() 返回的是[<UserModel 1>]这是一个列表 UserModel.query.filter_by(id=i).all()[0]取第一个值
            # print(list)
            if list.id != '':
                if list.status == 0:
                    Delete_tourist_list.append(
                        {"title": list.source_title, "msg": list.source_msg, "img": list.source_img, "status": list.status})
                else:
                    mysql_init_conn().close()
                    pass
            else:
                i = list.id
                mysql_init_conn().close()
                pass
            # append 列表添加{}大括号 json数据 把多个字典变成列表
    except:
        print("获取资源异常")
    # finally:
        # lock.release()
    mysql_init_conn().close()
    time.sleep(0.5)
    return jsonify(Delete_tourist_list)


@bp.route('/tourist_resources/detail', methods=['Get'])
def get_tourist_resources():
    mysql_init_conn()
    tourist_list = []
    # lock.acquire()
    # 获取参数值并赋值给res
    res = request.args
    # 获取
    title = res.get('title')
    msg = res.get('msg')
    # print(id+' '+title+' '+msg)
    # 定义为列表
    # try:
    # 查询该数据库长度(条数)
    # count = SourceModel.query.count()
    # print(count)
    list = SourceModel.query.filter_by(source_title=title)[0]
    if list:
        if list.source_msg == msg:
            # [0]列表 代表取第一个值
            # UserModel.query.filter_by(id=i).all() 返回的是[<UserModel 1>]这是一个列表 UserModel.query.filter_by(id=i).all()[0]取第一个值
            # print(list)
            if list.status == 1:
                tourist_list.append(
                    {"title": list.source_title, "msg": list.source_msg, "img": list.source_img, "status": list.status})
            else:
                mysql_init_conn().close()
                pass
            # append 列表添加{}大括号 json数据 把多个字典变成列表
        else:
            mysql_init_conn().close()
            time.sleep(0.5)
            return jsonify({"code":400,"msg":"文章不一致",'status':1})
    else:
        mysql_init_conn().close()
        time.sleep(0.5)
        return jsonify({"code":400,"msg":"不存在这条数据",'status':1})
    # except:
    #     print("获取资源异常")
    time.sleep(0.5)
    mysql_init_conn().close()
    return jsonify(tourist_list)
