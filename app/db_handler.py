from app.config import MAX_MEMROY_LEVEL_VALUE

from data.user import User
from data.word import Word

from data.db_session import global_init, create_session
from sqlalchemy.sql import exists

from time import time

global_init("db\database.sqlite")


def existence_of_user(telegram_id: int) -> bool:
    database_session = create_session()
    result = database_session.query(User).where(User.telegram_id == telegram_id).first()
    database_session.close()

    return bool(result)


def existence_of_word(telegram_id: int, russian_word: str) -> bool:
    database_session = create_session()
    result = database_session.query(Word).where(
        (Word.telegram_id == telegram_id) & (Word.russian_word == russian_word)
    ).first()
    database_session.close()

    return bool(result)


def add_user_to_database(telegram_id: int) -> None:
    if existence_of_user(telegram_id):
        return
    
    database_session = create_session()

    user = User()
    user.telegram_id = telegram_id

    database_session.add(user)
    database_session.commit()
    database_session.close()


def get_all_user_infromation(telegram_id: int) -> dict:
    add_user_to_database(telegram_id)

    database_session = create_session()

    user: User = database_session.query(User).where((User.telegram_id == telegram_id)).first()
    dictionary = user.__dict__.copy()

    database_session.commit()
    return dictionary


def set_translating_on_word(telegram_id: int, russian_word: str, foreign_word: str) -> None:
    database_session = create_session()
    word: Word = database_session.query(Word).where(
        (Word.telegram_id == telegram_id) & (Word.russian_word == russian_word)
    ).first()

    if word:
        word.foreign_word = foreign_word
        database_session.commit()

    database_session.close()


def get_word_dict_using_russian_word(telegram_id: int, russian_word: str) -> dict | None:
    database_session = create_session()
    word: Word = database_session.query(Word).where(
        (Word.telegram_id == telegram_id) & (Word.russian_word == russian_word)
    ).first()

    if word:
        result = word.__dict__.copy()
        database_session.close()

        return result

    database_session.close()


def get_all_user_words(telegram_id: int) -> list[Word]:
    database_session = create_session()
    words: list[Word] = list(database_session.query(Word).where(Word.telegram_id == telegram_id).all())

    if words:
        result = [word.__dict__.copy() for word in words]
        database_session.close()

        return result

    database_session.close()
    return []


def add_new_word_in_database(telegram_id: int, russian_word: str) -> None:
    database_session = create_session()

    if existence_of_word(telegram_id, russian_word):
        database_session.close()
        return 
    
    word = Word()
    word.telegram_id = telegram_id
    word.russian_word = russian_word

    database_session.add(word)
    database_session.commit()
    database_session.close()


def update_total_words_count(telegram_id: int) -> None:
    add_user_to_database(telegram_id)
    database_session = create_session()

    user: User = database_session.query(User).where((User.telegram_id == telegram_id)).first()
    user.total_count_of_words = len(get_all_user_words(telegram_id))

    database_session.commit()
    database_session.close()


def update_memory_level_of_word(telegram_id: int, russian_word: str, delta: int) -> None:
    database_session = create_session()

    user = database_session.query(User).where(User.telegram_id == telegram_id).first()
    word = database_session.query(Word).where(
        (Word.telegram_id == telegram_id) & (Word.russian_word == russian_word)
    ).first()

    if word is None:
        database_session.close()
        return
    
    if delta > 0:
        user.count_of_correctly_translated_words += 1
    else:
        user.count_of_incorrectly_translated_words += 1
    
    word.memory_level = min(max(0, word.memory_level + delta), MAX_MEMROY_LEVEL_VALUE)
    
    database_session.commit()
    database_session.close()


def reset_all_levels_of_memory(telegram_id: int) -> None:
    database_session = create_session()

    words: list[Word]= database_session.query(Word).where(Word.telegram_id == telegram_id).all()

    for word in words:
        word.memory_level = 0

    database_session.commit()
    database_session.close()