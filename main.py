from app.bot_object import bot

from app.commands.start import start_command
from app.commands.add_word import add_word_command
from app.commands.train import train_command

from app.handlers import message_handler


if __name__ == "__main__":
    bot.polling(none_stop=True)
