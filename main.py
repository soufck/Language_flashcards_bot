from sqlalchemy import create_engine, Column, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import telebot
from telebot import types
from googletrans import Translator
from random import choice

TEXT_INPUT = False
TEXT_CHANGE = False
workout = False
Base = declarative_base()
first_id_word = 0


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    russian_word = Column(String, nullable=True)
    foreign_word = Column(String, nullable=True)
    memory_level = Column(Integer, nullable=True)
    count_shows = Column(Integer, nullable=True)
    count_false_shows = Column(Integer, nullable=True)
    fail_ans = Column(Integer, nullable=True)

    def __init__(self, russian_word, foreign_word, memory_level, count_shows, count_false_shows, fail_ans):
        self.russian_word = russian_word
        self.foreign_word = foreign_word
        self.memory_level = memory_level
        self.count_shows = count_shows
        self.count_false_shows = count_false_shows
        self.fail_ans = fail_ans

    def __repr__(self):
        return f"{self.id}, {self.russian_word}, {self.foreign_word}. {self.memory_level}"


engine = create_engine('sqlite:///users.db', echo=False)

Base.metadata.create_all(bind=engine)


def change_word(list_change, translate=False) -> str:
    Session = sessionmaker(bind=engine)
    session = Session()
    if translate:
        word_id, russian = list_change
        word_id = int(word_id)
        word = session.query(Word).get(word_id)
        word.russian_word = russian
        word.foreign_word = translation(russian)
    if not translate:
        word_id, russian, foreign = list_change
        word_id = int(word_id)
        word = session.query(Word).get(word_id)
        word.russian_word = russian
        word.foreign_word = foreign
    session.commit()
    return ":".join(get_word_by_id(word_id, strs=True))


def create_word(russian_word, foreign_word, memory_level=1) -> None:
    Session = sessionmaker(bind=engine)
    session = Session()
    word = Word(russian_word=russian_word, foreign_word=foreign_word, memory_level=memory_level,
                count_shows=4, count_false_shows=2, fail_ans=0)
    session.add(word)
    session.commit()
    session.close()


def translation(russian_word) -> str:
    trans = Translator()
    return trans.translate(russian_word).text


def delete(word_id) -> None:
    Session = sessionmaker(bind=engine)
    session = Session()
    word = session.query(Word).get(id=word_id)
    session.delete(word)
    session.commit()
    session.close()


def get_word_by_id(word_id, strs=False) -> list:
    Session = sessionmaker(bind=engine)
    session = Session()
    word = session.query(Word).get(word_id)
    list_data = [word.id, word.russian_word, word.foreign_word]
    session.close()
    if strs:
        list_data[0] = str(word.id)
        return list_data
    return list_data


def get_amount_of_words(memory=False, shows=False, false_shows=False, fail_ans=False) -> list:
    Session = sessionmaker(bind=engine)
    session = Session()
    ans = [word.id for word in session.query(Word.id).all()]
    if memory:
        ans.append([word.memory_level for word in session.query(Word).all()])
    if shows:
        ans.append(word.count_shows for word in session.query(Word).all())
    if false_shows:
        ans.append(word.count_false_shows for word in session.query(Word).all())
    if fail_ans:
        ans.append(word.fail_ans for word in session.query(Word).all())
    session.close()
    return ans


def show_dictionary() -> list:
    list_id = get_amount_of_words()[0]
    list_data = []
    for word_id in list_id:
        list_data.append(":".join(get_word_by_id(word_id, strs=True)))
    return list_data


def get_random_word():
    Session = sessionmaker(bind=engine)
    session = Session()
    word = session.query(Word).order_by(func.random()).first()
    session.close()
    return word


def update_word_stats(word, is_correct):
    Session = sessionmaker(bind=engine)
    session = Session()
    if is_correct:
        word.count_shows += 1
        if word.count_shows == 4:
            word.memory_level = 0
    else:
        word.count_false_shows += 1
        word.memory_level = 2
        word.fail_ans += 1
    session.commit()

def next_word(message):
        word = get_random_word()
        if word:
            bot.send_message(message.chat.id, f"What is the English translation of '{word.russian_word}'?")
        else:
            bot.send_message(message.chat.id, "No words available in the database.")

def check_translation(message):
        Session = sessionmaker(bind=engine)
        session = Session()
        word = session.query(Word).filter_by(russian_word=message.text).first()
        if word:
            update_word_stats(word, is_correct=True)
            bot.send_message(message.chat.id, "Correct translation!")
        else:
            bot.send_message(message.chat.id, "Incorrect translation!")
        session.close()
        next_word(message)


bot = telebot.TeleBot("6988140564:AAFbjveyolIdsj3GQ5hk8bh0wQzSzM84KqM")


@bot.message_handler(commands=["start"])
def start(message):
    strs = "Добро пожаловать в бот флеш карточки"
    group = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Словари")
    btn2 = types.KeyboardButton("Тренировка")
    group.add(btn2, btn1)
    bot.send_message(message.chat.id, strs, reply_markup=group)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    global TEXT_INPUT, TEXT_CHANGE, workout
    if TEXT_INPUT:
        TEXT_INPUT = False
        group = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Добавить")
        btn2 = types.KeyboardButton("Редактировать")
        btn4 = types.KeyboardButton("Назад")
        btn3 = types.KeyboardButton("Выбрать")
        group.add(btn1, btn2)
        group.add(btn3, btn4)
        words = message.text.split()
        for word in words:
            create_word(word, translation(word))
        bot.send_message(message.chat.id, "Слова успешно добавлены, пожалуйста проверьте словарь",
                         reply_markup=group)
        for word in show_dictionary():
            bot.send_message(message.chat.id, word)

    if TEXT_CHANGE:
        if len(message.text.split(":")) == 2:
            word = change_word(message.text.split(":"), translate=True)
        if len(message.text.split(":")) == 3:
            word = change_word(message.text.split(":"))
        group = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Добавить")
        btn2 = types.KeyboardButton("Редактировать")
        btn4 = types.KeyboardButton("Назад")
        btn3 = types.KeyboardButton("Выбрать")
        group.add(btn1, btn2)
        group.add(btn3, btn4)
        bot.send_message(message.chat.id, "Изменения пременены" + "\n" + word, reply_markup=group)
        TEXT_CHANGE = False

    if workout:
        if message.text == "Начать тренировку":
            word = get_random_word()
            if word:
                bot.send_message(message.chat.id, f"What is the English translation of '{word.russian_word}'?")
            else:
                bot.send_message(message.chat.id, "No words available in the database.")
        elif message.text == "Continue available":
            words = show_dictionary()
            for word in words:
                bot.send_message(message.chat.id, word)
            group = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_start = types.KeyboardButton("Start Workout")
            group.add(btn_start)
            bot.send_message(message.chat.id, "Click 'Start Workout' to begin training.", reply_markup=group)
        elif message.text == "Next":
            next_word(message)
        else:
            check_translation(message)

    if not TEXT_INPUT and not TEXT_CHANGE and not workout:
        if message.text == "Словари":
            group = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Добавить")
            btn2 = types.KeyboardButton("Редактировать")
            btn4 = types.KeyboardButton("Назад")
            btn3 = types.KeyboardButton("Выбрать")
            group.add(btn1, btn2)
            group.add(btn3, btn4)
            bot.send_message(message.chat.id, "Введите слова для изучения через пробел", reply_markup=group)

        elif "Добавить" in message.text:
            TEXT_INPUT = True
            bot.send_message(message.chat.id, "Введите слова через пробел", reply_markup=types.ReplyKeyboardRemove())

        elif message.text == "Редактировать":
            TEXT_CHANGE = True
            data = show_dictionary()
            bot.send_message(message.chat.id, "Впишите изменения в формате:\n"
                                              "'номер строки:"
                                              "слово на основном языке:"
                                              "слово на изучаемом языке'")
            for string in data:
                bot.send_message(message.chat.id, string)

        elif message.text == "Тренировка":
            group = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn3 = types.KeyboardButton("Подробный отчет")
            btn4 = types.KeyboardButton("Назад")
            btn5 = types.KeyboardButton("Начать")
            group.add(btn5)
            group.add(btn3, btn4)
            bot.send_message(message.chat.id, "Нажмите начать для начала тренировки", reply_markup=group)

        elif message.text == "Начать":
            workout = True
            group = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn3 = types.KeyboardButton("Next")
            group.add(btn3)
            bot.send_message(message.chat.id, "Click 'Next' to begin.", reply_markup=group)

        elif message.text == "Назад":
            group1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Словари")
            btn2 = types.KeyboardButton("Тренировка")
            group1.add(btn2, btn1)
            bot.send_message(message.chat.id, ",,,", reply_markup=group1)

        elif (message.text == "Закончить"):
            group = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn3 = types.KeyboardButton("Подробный отчет")  # статистика: % выполнения и самые проблемные слова
            #  можем сделать рекомендуемый словарь, с проблемными не выученными словами
            btn4 = types.KeyboardButton("Назад")
            btn5 = types.KeyboardButton("Начать")
            group.add(btn5)
            group.add(btn3, btn4)
            bot.send_message(message.chat.id, "тут должен быть процент выполнения", reply_markup=group)


        elif (message.text == "Подробный отчет"):
            group = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Посмотрел")
            group.add(btn1)
            bot.send_message(message.chat.id, "статистика: % выполнения и топ самыйх плохо отвечаемых слов",
                             reply_markup=group)

        elif (message.text == "Посмотрел"):
            group = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn3 = types.KeyboardButton(
                "Подробный отчет")  # статистика: % выполнения и топ самыйх плохо отвечаемых слов
            btn4 = types.KeyboardButton("Назад")
            btn5 = types.KeyboardButton("Начать")
            group.add(btn5)
            group.add(btn3, btn4)
            bot.send_message(message.chat.id, "Нажмите начать для начала тренировки", reply_markup=group)


if __name__ == "__main__":
    bot.polling()
