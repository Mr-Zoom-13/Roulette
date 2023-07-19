import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String)
    log_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('logs.id'))
    log = orm.relationship('Log', back_populates="users")
    photo = sqlalchemy.Column(sqlalchemy.String)
    summ = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    prc = sqlalchemy.Column(sqlalchemy.Float)
