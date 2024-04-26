from app.bot_object import bot
from app.commands.add_word.add_word_command import add_word_to_database_step_1
from app.commands.train.train_command import *
from app.commands.statistic.statistic_command import * 

from telebot.types import Message


@bot.message_handler(func=lambda message: True)
def global_message_hanlder(message: Message) -> None:
    text = message.text

    if text == "Тренировка 🎮":
        train_command_step_1(message)
    elif text == "Добавить слово ➕":
        add_word_to_database_step_1(message)
    elif text == "Статистика 📈":
        statistic_command(message)
