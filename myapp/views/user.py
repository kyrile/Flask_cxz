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
    if request.method == 'POST':
        nick_name = request.form.get('nick_name')
        password = request.form.get('password')
        # 修改用户信息
        user.nick_name = nick_name
        user.auth_key = password
        # db.session.commit()
    return render_template('user/info.html',
                           user=user)

# ajax头像上传
@blue.route('/upload', methods=['POST'])
def upload_photo():
    upload_file: FileStorage = request.files.get('photo')

    filename = uuid.uuid4().hex + os.path.splitext(upload_file.filename)[-1]
    filepath = os.path.join(settings.USER_DIR, filename)

    upload_file.save(filepath)

    user = User.query.get(cache.get_user_id(request.cookies.get('token')))
    # 任务1：删除之前的用户头像
    if user.photo:
        pre_img = os.path.join(settings.USER_DIR, user.photo.split('/')[1])
        os.remove(pre_img)

    # 修改新头像的路径
    user.photo = 'user/' + filename
    # db.session.commit()

    # ? 图片如何压缩- PIL(pip install pillow)

    return jsonify({
        'msg': '上传成功',
        'path': 'user/' + filename,
    })


# 用户登录功能
@blue.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        nick_name = request.form.get('nick_name')
        passwd = request.form.get('passwd')
        # 去数据库查询是否有此用户
        login_user = User.query.filter(User.nick_name == nick_name,
                                      User.auth_key == passwd).first()
        if login_user:
            # 登录成功
            # 生成token
            token = uuid.uuid4().hex
            resp = redirect('/')
            resp.set_cookie('token', token, expires=(datetime.now() + timedelta(days=3)))
            # 将token添加到redis, token-user_id
            cache.save_token(token, login_user.id)
            return resp
        else:
            message = '查无此用户'

    return render_template('user/login.html', msg=message)