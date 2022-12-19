from flask import (Blueprint,
                   request,
                   session,
                   redirect,
                   jsonify,
                   g,
                   json,

                   )
import time
import os
# import re
# import base64
from form import UpsourceForm
from model import SourceModel,db
from exts import Conn,loggerInfo,loggerError,loggerWarning,get_time,get_request_ip

bp = Blueprint('source', __name__, url_prefix="/source")


@bp.route('/addpicture', methods=['POST','GET'])
def post_addpicture():
    try:
        # form = UpsourceForm(request.form)
        # return jsonify({"code": 200, "msg": "上传成功", "status": 1})
        if request.method == 'GET':
            pass
        else:
            filepirture = request.files["file"]
            # 获取文件

            file = request.files.get("file")
            # 获取文件

            # file_pirture = file.read()

            # print(file.filename)

            buffer_pirture = filepirture.read()
            # 读取二进制文件

            # print(file)

            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            image_path = 'D:\py项目\Vue_flask_python\static\images/' + file.filename
            with open(image_path, "wb") as w:  # 使用with open()新建对象f
                w.write(buffer_pirture)  # 写入数据，文件保存在上面指定的目录，加\n为了换行更方便阅读
            # print("写入文件成功")
            loggerError(get_time()+' '+' '+get_request_ip(request)+' '+str("写入图片成功"))
            w.close()
            return jsonify({"code": 200, "msg": "上传图片成功", "status": 1})
    except Exception as e:
        loggerError(get_time()+' '+' '+get_request_ip(request)+' '+str(e))

@bp.route('/addSource', methods=['POST','GET'])
def post_addSource():
    Conn()
    try:
        form = UpsourceForm(request.form)
        # return jsonify({"code": 200, "msg": "上传成功", "status": 1})
        # form = request.form
        if request.method == 'POST':
            if form.validate():
                picture_title = form.title.data
                picture_msg = form.msg.data
                img_name = form.name.data
                # print(picture_msg,img_name,picture_title)
                # picture_title = form.get('title')
                # picture_msg = form.get('msg')
                # img_name =  form.get('name')
                image_path = 'D:\py项目\Vue_flask_python\static\images\picture_'  +  img_name
                if image_path:
                    try:
                        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        Source = SourceModel(source_msg=picture_msg, source_title=picture_title, source_img=image_path, status=1,
                                             create_time=create_time, update_time=create_time)
                        db.session.add(Source)
                        db.session.commit()
                        return jsonify({"code": 200, "msg": "上传成功", "status": 1})
                    except Exception as e:
                        loggerError(get_time()+' '+' '+get_request_ip(request)+' '+str(e))
                        return jsonify({"code": 400, "msg": "上传失败，数据库上传异常", "status": 1})
                else:
                    return jsonify({"code": 400, "msg": "上传失败，图片未上传成功", "status": 1})
            else:
                return jsonify({"code": 400, "msg": "表单验证失败，请检查！", "status": 1})
        else:
            return jsonify({"code": 400, "msg": "非法请求，请检查！", "status": 1})
    except Exception as e:
        loggerError(get_time()+' '+' '+get_request_ip(request)+' '+str(e))


@bp.route('/DeleteSource', methods=['POST'])
def post_DeleteSource():
    Conn()
    try:
        da = request.get_data()
        # print(da)
        data = json.loads(da)  # json.loads 把传回来的值整成字典
        # sourceuser = data['user']
        sourcemsg = data['msg']
        up_time = get_time()
        # 修改数据 删除账户把账户状态值设为0
        sourcecache = SourceModel.query.filter_by(source_msg=sourcemsg)[0]
        sourcecache.status = 0
        sourcecache.update_time = up_time
        db.session.commit()
        Conn().close()
        loggerInfo(get_time() +" " + get_request_ip(request)+" " + "请求删除失败")
        return jsonify({"code": 200, "msg": "删除成功", "status": 1})
    except Exception as e:
        loggerError(get_time() + ' ' + ' ' + get_request_ip(request) + ' ' + str(e))

@bp.route('/RecoverSource', methods=['POST'])
def post_RecoverSource():
    Conn()
    try:
        da = request.get_data()
        # print(da)
        data = json.loads(da)  # json.loads 把传回来的值整成字典
        # sourceuser = data['user']
        sourcemsg = data['msg']
        up_time = get_time()
        # 修改数据 删除账户把账户状态值设为0
        sourcecache = SourceModel.query.filter_by(source_msg=sourcemsg)[0]
        sourcecache.status = 1
        sourcecache.update_time = up_time
        db.session.commit()
        Conn().close()
        loggerInfo(get_time()+ " " + get_request_ip(request)+ " " + "请求恢复资源成功")
        return jsonify({"code": 200, "msg": "恢复成功", "status": 1})
    except Exception as e:
        loggerError(get_time() + ' ' + ' ' + get_request_ip(request) + ' ' + str(e))

@bp.route('/tourist_resources', methods=['Get'])
def get_tourist_sources():
    Conn()
    try:
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
                    pass
            else:
                i = list.id
                pass
            # append 列表添加{}大括号 json数据 把多个字典变成列表
        # except:
        #     print("获取资源异常")
        Conn().close()
        loggerInfo(get_time()+" " + get_request_ip(request)+ " "+ "请求获取资源成功")
    except Exception as e:
        loggerError(get_time() + ' ' + ' ' + get_request_ip(request) + ' ' + str(e))
    return jsonify(tourist_list)

@bp.route('/Delete_tourist_resources', methods=['Get'])
def get_Delete_tourist_sources():
    Conn()
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
                    pass
            else:
                i = list.id
                pass

            # append 列表添加{}大括号 json数据 把多个字典变成列表
    except Exception as e:
        loggerError(get_time() + ' ' + ' ' + get_request_ip(request) + ' ' + str(e))
    Conn().close()
    loggerInfo(get_time()+ " "+ get_request_ip(request)+" " + "请求获取删除列表成功")
    return jsonify(Delete_tourist_list)


@bp.route('/tourist_resources/detail', methods=['Get'])
def get_tourist_resources():
    tourist_list = []
    # 获取参数值并赋值给res
    res = request.args
    # 获取
    id = res.get('id')
    title = res.get('title')
    msg = res.get('msg')
    # 定义为列表
    # try:
    # 查询该数据库长度(条数)
    # count = SourceModel.query.count()
    # print(count)
    Conn()
    try:
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
                    pass
                # append 列表添加{}大括号 json数据 把多个字典变成列表
            else:
                return jsonify({"code":400,"msg":"文章不一致",'status':1})
        else:
            return jsonify({"code":400,"msg":"不存在这条数据",'status':1})
        # except:
        #     print("获取资源异常")
        loggerInfo(get_time()+" " + get_request_ip(request) + " "+ "请求获取资源细节成功")
        Conn().close()
    except Exception as e:
        print("资源细节获取失败：%s" %e)
        loggerError(get_time() + ' ' + ' ' + get_request_ip(request) + ' ' + str(e))
    return jsonify(tourist_list)