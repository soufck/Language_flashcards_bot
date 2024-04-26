from app.bot_object import bot
from app.db_handler import add_user_to_database
from app.commands.start.start_texts import greeting_text
from app.commands.start.start_markups import greeting_markup

from telebot.types import Message


@bot.message_handler(commands=["start"])
def greeting(message: Message) -> None:
    add_user_to_database(message.from_user.id)
    bot.send_message(message.from_user.id, greeting_text, reply_markup=greeting_markup)
