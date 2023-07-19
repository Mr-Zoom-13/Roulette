import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from datetime import datetime



class Log(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'logs'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    users = orm.relationship('User', back_populates='log')
    winner_id = sqlalchemy.Column(sqlalchemy.Integer)
    summ = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    com = sqlalchemy.Column(sqlalchemy.Integer, default=20)
    datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

