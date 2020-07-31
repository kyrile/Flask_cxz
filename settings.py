from urllib.parse import quote_plus as cxz_plus
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.join(PROJECT_DIR, 'myapp')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
USER_DIR = os.path.join(STATIC_DIR, 'user')


class Dev():
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:%s@192.168.43.112:13306/py_test?charset=utf8&autocommit=true' % cxz_plus('cxz@123')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = True


