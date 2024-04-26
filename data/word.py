from .db_session import SqlAlchemyBase

from sqlalchemy import Column
from sqlalchemy import Integer, String


class Word(SqlAlchemyBase):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False)
    russian_word = Column(String, nullable=True)
    foreign_word = Column(String, nullable=True)
    memory_level = Column(Integer, default=0)
