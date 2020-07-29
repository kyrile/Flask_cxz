from datetime import datetime, timedelta
import uuid

from flask import render_template, request, redirect
from flask import Blueprint

from models.user import User
from utils import crypt, cache

blue = Blueprint('userBlue', __name__)


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