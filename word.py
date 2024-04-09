import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Word(SqlAlchemyBase):
    __tablename__ = 'words'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    russian_word = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    foreigh_word = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    memory_level = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
