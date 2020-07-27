from urllib.parse import quote_plus as cxz_plus


class Dev():
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:%s@192.168.43.112:13306/py_test?charset=utf8&autocommit=true' % cxz_plus('cxz@123')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = True


