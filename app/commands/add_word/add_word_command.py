from googletrans import Translator

from app.bot_object import bot
from app.db_handler import *
from app.commands.add_word.add_word_texts import choose_word_text
from app.commands.add_word.add_word_markup import generate_choose_word_markup, confrimed_markup

from telebot.types import Message, CallbackQuery

translating_function = Translator().translate
__CALLBACK_QUERY_COMMANDS = [
    "USE_MY_TRANSLATING",
    "USE_BOT_TRANSLATING",
    "CONFIRMED"
]


@bot.message_handler(commands=["add_word"])
def add_word_to_database_step_1(message: Message) -> None:
    add_user_to_database(message.from_user.id)
    send = bot.send_message(message.from_user.id, "Напишите Ваше слово на русском языке")
    bot.register_next_step_handler(send, add_word_to_database_step_2)


def add_word_to_database_step_2(message: Message) -> None:
    add_new_word_in_database(message.from_user.id, message.text)
    send = bot.send_message(message.from_user.id, "Напишите Ваше слово на английском языке")
    bot.register_next_step_handler(send, add_word_to_database_step_3, message.text)


def add_word_to_database_step_3(message: Message, russian_word: str) -> None:
    owner_english_word, recomended_english_word = message.text, translating_function(russian_word).text
    bot.send_message(
        chat_id=message.from_user.id,
        text=choose_word_text(russian_word, owner_english_word, recomended_english_word),
        reply_markup=generate_choose_word_markup(russian_word, owner_english_word, recomended_english_word),
        parse_mode="HTML"
    )


@bot.message_handler(commands=["delete_word"])
def delete_word_from_database_step_1(message: Message) -> None:
    add_user_to_database(message.from_user.id)
    send = bot.send_message(message.from_user.id, "Напишите слово на русском, которое необходимо удалить")
    bot.register_next_step_handler(send, delete_word_from_database_step_2)


def delete_word_from_database_step_2(message: Message) -> None:
    if delete_word_from_database(telegram_id=message.from_user.id, russian_word=message.text):
        bot.send_message(message.from_user.id, f"Слово <code>{message.text}</code> было успешно удалено 😌", parse_mode="HTML")
    else:
        bot.send_message(message.from_user.id, f"Слова <code>{message.text}</code> нет в БД 😟", parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: any([call.data.startswith(command) for command in __CALLBACK_QUERY_COMMANDS]))
def callback_query_word_adding_handler(call: CallbackQuery) -> None:
    data = call.data 

    if data.startswith("USE_MY_TRANSLATING") or data.startswith("USE_BOT_TRANSLATING"):
        russian_word, foreign_word = data.split(';')[1:3]
        set_translating_on_word(telegram_id=call.from_user.id, russian_word=russian_word, foreign_word=foreign_word)

        bot.answer_callback_query(callback_query_id=call.id, text="Ваше слово было успешно занесено в БД ☺️", show_alert=True)
        bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.id,
            reply_markup=confrimed_markup
        )
    elif data == "CONFIRMED":
        bot.answer_callback_query(callback_query_id=call.id, text="Данное слово уже добавлено в БД 😓", show_alert=True)
