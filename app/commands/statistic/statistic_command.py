from app.bot_object import bot
from app.db_handler import get_all_user_infromation, update_total_words_count
from app.commands.statistic.statistic_texts import generate_human_statistic_text

from telebot.types import Message


@bot.message_handler(commands=["statistic"])
def statistic_command(message: Message) -> None:
    update_total_words_count(message.from_user.id)
    user_infromation = get_all_user_infromation(message.from_user.id)
    bot.send_message(
        chat_id=message.from_user.id,
        text=generate_human_statistic_text(user_infromation),
        parse_mode="HTML"
    )
