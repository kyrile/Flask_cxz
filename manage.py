from flask_script import Manager
from models.user import db, User
from myapp import app
from myapp.views import index


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
    db.init_app(app)
    manager = Manager(app)
    manager.run()