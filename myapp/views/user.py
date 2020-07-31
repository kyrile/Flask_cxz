import os
from datetime import datetime, timedelta
import uuid

from flask import render_template, request, redirect, jsonify
from flask import Blueprint
from werkzeug.datastructures import FileStorage

import settings
from models import db
from models.user import User
from utils import crypt, cache

blue = Blueprint('userBlue', __name__)


# 修改用户信息
@blue.route('/modify', methods=['GET', 'POST'])
def modify():
    token = request.cookies.get('token')
    user_id = cache.get_user_id(token)

    # 任务2： 优化登录用户的相关信息存在redis中(缓存)
    user = User.query.get(int(user_id))

    msg = ''
    if request.method == 'POST':
        # 头像上传
        # 获取上传的文件
        # user_photo必须和前端请求中文件字段名保持一致
        upload_file: FileStorage = request.files.get('user_photo')
        print('文件名： ', upload_file.filename)
        # print('文件长度（字节）： ', upload_file.content_length)
        print('文件类型： ', upload_file.content_type)
        # 验证文件是否为图片
        if not upload_file.content_type.startswith('image/'):
            msg = '只支持图片上传'
        else:
            # 保存图片
            filename = uuid.uuid4().hex + os.path.splitext(upload_file.filename)[-1]
            filepath = os.path.join(settings.USER_DIR, filename)

            # 服务端保存上传的文件
            upload_file.save(filepath)

            # 更新用户信息
            # 保存在数据库的图片是相对static资源访问的路径
            user.photo = 'user/' + filename
            db.session.commit()

    return render_template('user/info.html',
                           user=user,
                           msg=msg)


@blue.route('/upload', methods=['POST'])
def upload_photo():
    upload_file: FileStorage = request.files.get('photo')

    filename = uuid.uuid4().hex + os.path.splitext(upload_file.filename)[-1]
    filepath = os.path.join(settings.USER_DIR, filename)

    upload_file.save(filepath)

    user = User.query.get(cache.get_user_id(request.cookies.get('token')))
    # 任务1： 删除之前的用户头像

    user.photo = 'user/' + filename
    db.session.commit()

    # ? 图片如何压缩- PIL(pip install pillow)

    return jsonify({
        'msg': '上传成功',
        'path': 'user/' + filename
    })


# 用户登录功能
@blue.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        phone = request.form.get('phone')
        passwd = request.form.get('passwd')
        # 去数据库查询是否有此用户
        login_user = User.query.filter(User.phone == phone,
                                      User.auth_key == passwd).first()
        if login_user:
            # 登录成功
            # 生成token
            token = uuid.uuid4().hex  #
            resp = redirect('/')
            resp.set_cookie('token', token, expires=(datetime.now() + timedelta(days=3)))

            # 将token添加到redis, token-user_id
            cache.save_token(token, login_user.id)
            return resp
        else:
            message = '查无此用户'

    return render_template('user/login.html', msg=message)