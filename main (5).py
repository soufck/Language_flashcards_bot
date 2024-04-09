from data import db_session
from data.word import Word
import requests as rp


def create_word(russian_word, foreigh_word, memory_level=1): # 0 - слово не встречается в обороте;
    # 1 - обычное чило повторений; 2 - учащенное чило повторений
    word = Word()
    word.russian_word = russian_word
    word.foreigh_word = foreigh_word
    word.memory_level = memory_level
    return word


def delete_word(id):
    word = Word()
    word.id = id


def main():
    db_session.global_init('flash_cards.db')
    db_sess = db_session.create_session()
    new_word = create_word('депрессия',
                           rp.post("http://127.0.0.1:8080/submit", data={"word": "депрессия", "scr": "ru"}).text)
    db_sess.add(new_word)
    # слова удаляются по запросу пользователя, а не после первого верного ответа, через отдельную функцию из бота 
    for word in db_sess.query(Word).filter(Word.memory_level == 0):
        word.delete()
    db_sess.commit()


if __name__ == '__main__':
    main()
