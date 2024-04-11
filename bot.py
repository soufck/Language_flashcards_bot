import telebot
from telebot import types

bot = telebot.TeleBot("6988140564:AAFbjveyolIdsj3GQ5hk8bh0wQzSzM84KqM")


@bot.message_handler(commands=["start"])
def start(massage):
    strs = "Добро пожаловать в бот флеш карточки бла бла бла"
    group = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Словари")
    btn2 = types.KeyboardButton("Тренировка")
    group.add(btn2, btn1)
    bot.send_message(massage.chat.id, strs, reply_markup=group)


@bot.message_handler(content_types=['text'])
def dicts(massage):
    if (massage.text == "Словари"):
        group = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Добавить")
        btn2 = types.KeyboardButton("Редактировать")
        btn4 = types.KeyboardButton("Назад")
        btn3 = types.KeyboardButton("Выбрать")
        group.add(btn1, btn2)
        group.add(btn3, btn4)
        bot.send_message(massage.chat.id, "Введите слова для изучения через пробел", reply_markup=group)


    elif (massage.text == "Тренировка"):
        group = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton("Подробный отчет")  # статистика: % выполнения и топ самыйх плохо отвечаемых слов
        btn4 = types.KeyboardButton("Назад")
        btn5 = types.KeyboardButton("Начать")
        group.add(btn5)
        group.add(btn3, btn4)
        bot.send_message(massage.chat.id, "Нажмите начать для начала тренировки", reply_markup=group)


    elif (massage.text == "Начать"):
        group = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Верно")
        btn2 = types.KeyboardButton("Неверно")
        btn3 = types.KeyboardButton("Закончить")
        group.add(btn1, btn2)
        group.add(btn3)
        bot.send_message(massage.chat.id, "......", reply_markup=group) # тут должны быть слова из алгортма по работе с бд


    elif (massage.text == "Назад"):
        group1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Словари")
        btn2 = types.KeyboardButton("Тренировка")
        group1.add(btn2, btn1)
        bot.send_message(massage.chat.id, ",,,", reply_markup=group1)


    elif (massage.text == "Закончить"):
        group = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton("Подробный отчет")  # статистика: % выполнения и самые проблемные слова
        #  можем сделать рекомендуемый словарь, с проблемными не выученными словами
        btn4 = types.KeyboardButton("Назад")
        btn5 = types.KeyboardButton("Начать")
        group.add(btn5)
        group.add(btn3, btn4)
        bot.send_message(massage.chat.id, "......", reply_markup=group)  # тут должен быть процент выполнения


    elif (massage.text == "Посмотрел"):
        group = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton("Подробный отчет")  # статистика: % выполнения и топ самыйх плохо отвечаемых слов
        btn4 = types.KeyboardButton("Назад")
        btn5 = types.KeyboardButton("Начать")
        group.add(btn5)
        group.add(btn3, btn4)
        bot.send_message(massage.chat.id, "Нажмите начать для начала тренировки", reply_markup=group)


    elif (massage.text == "Подробный отчет"):
        group = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Посмотрел")
        group.add(btn1)
        bot.send_message(massage.chat.id, "Нажмите начать для начала тренировки", reply_markup=group)

    # Словарь
    # # кнопка для создания словаря
    # # кнопка выбора словаря
    # # кнопка удаления словаря
    # кнопка начала тренировки
    # # старт
    # # конец


bot.polling()
