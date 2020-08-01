from flask import request, redirect, url_for
from flask_script import Manager
from models.user import db, User
from myapp import app
from myapp.views import index, user
from utils import cache


@app.before_request
def check_login():
    app.logger.info(request.path+'被访问了')
    if request.path not in ['/user/login',
                             '/log']:
        # 判断request中是否包含token
        # 验证token是否有效
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('userBlue.login'))
        else:
            user_id = cache.get_user_id(token)
            if not user_id:
                return redirect(url_for('userBlue.login'))


@app.route('/create_db', methods=['GET'])
def create_database():
    db.create_all()
    return "创建数据库中的所有模型表成功"


@app.route('/drop_db', methods=['GET'])
def drop_database():
    db.drop_all()
    return "drop数据库中的所有模型表成功"


if __name__ == '__main__':
    app.register_blueprint(index.blue)
    app.register_blueprint(user.blue, url_prefix='/user')
    db.init_app(app)
    manager = Manager(app)
    manager.run()