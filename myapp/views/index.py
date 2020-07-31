from flask import render_template, request
from flask import Blueprint

from models.user import User
from utils import cache

blue = Blueprint('indexBlue', __name__)


@blue.route('/')
def index():
    # 获取用户登录的信息
    token = request.cookies.get('token')
    user_id = cache.get_user_id(token)
    user = User.query.get(int(user_id))

    return render_template('index.html', user=user)
