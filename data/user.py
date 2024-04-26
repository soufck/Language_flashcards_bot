from sqlalchemy import Column, Integer
from datetime import datetime
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False)
    count_of_correctly_translated_words = Column(Integer, default=0)
    count_of_incorrectly_translated_words = Column(Integer, default=0)
    total_count_of_words = Column(Integer, default=0)
