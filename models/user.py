from sqlalchemy import Column, Integer, String, ForeignKey

from models import db

user_role = db.Table('user_role',
                     Column('user_id',Integer, ForeignKey('user.id', name='user_role_fk')),
                     Column('role_id',Integer, ForeignKey('role.id', name='user_role_pk')),
                     )


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)


class Role(BaseModel):
    __tablename__ = 'role'


class Qx(BaseModel):
    __tablename__ = 'qx'


class User(db.Model):
    id = Column(Integer,
                primary_key=True,
                autoincrement=True)
    phone = Column(String(20),
                   unique=True,
                   nullable=False)
    auth_key = Column(String(100), nullable=False)
    nick_name = Column(String(20))
    photo = Column(String(100))
    # Many-to-Many 多对多的关系，指定secondary设置关联的表，Table()
    roles = db.relationship(Role, secondary=user_role)