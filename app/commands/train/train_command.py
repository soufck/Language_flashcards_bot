from app.bot_object import bot
from app.config import MAX_MEMROY_LEVEL_VALUE

from app.db_handler import get_all_user_words, update_memory_level_of_word, reset_all_levels_of_memory
from app.commands.train.train_texts import correct_checking_text, how_it_can_be_translated
from app.commands.train.train_markups import *

from telebot.types import Message, CallbackQuery

from random import choice

__CALLBACK_QUERY_COMMANDS = [
    "RESET",
    "NEXT",
    "CORRECT",
    "INCORRECT",
    "+",
    "-"
]


@bot.message_handler(commands=["train"])
def train_command_step_1(message: Message | CallbackQuery) -> None:
    try:
        word = choice([*filter(lambda x: x["memory_level"] < MAX_MEMROY_LEVEL_VALUE, get_all_user_words(message.from_user.id))])
    except IndexError:
        words = get_all_user_words(message.from_user.id)

        if words:
            bot.send_message(
                chat_id=message.from_user.id,
                text="Вы успешно закрыли все слова!" + "\n" + "Чтобы начать снова нажмите <i>сброс</i>",
                reply_markup=reset_markup,
                parse_mode="HTML"
            )
        else:
            bot.send_message(message.from_user.id, "У вас пока что нет слов 😔")

        return
    
    send = bot.send_message(message.from_user.id, how_it_can_be_translated(word["russian_word"]), parse_mode="HTML")
    bot.register_next_step_handler(send, train_command_step_2, word)


def train_command_step_2(message: Message, word: dict) -> None:
    bot.send_message(
        chat_id=message.from_user.id,
        text=correct_checking_text(message.text, word["foreign_word"]),
        reply_markup=generate_train_markup(word["russian_word"]),
        parse_mode="HTML"
    )


@bot.callback_query_handler(func=lambda call: any([call.data.startswith(command) for command in __CALLBACK_QUERY_COMMANDS]))
def callback_query_train_handler(call: CallbackQuery) -> None:
    data = call.data 

    if data.startswith("CORRECT"):
        word = data.split(';')[-1]
        update_memory_level_of_word(
            telegram_id=call.from_user.id,
            russian_word=word,
            delta=1
        )

        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.id,
            reply_markup=correct_with_go_next_markup
        )
    elif data.startswith("INCORRECT"):
        word = data.split(';')[-1]
        update_memory_level_of_word(
            telegram_id=call.from_user.id,
            russian_word=word,
            delta=-1
        )

        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.id,
            reply_markup=incorrect_with_fo_next_markup
        )
    elif data in ['+', '-']:
        bot.answer_callback_query(callback_query_id=call.id, text="Ваш голос на этот вопрос уже учтён 😉", show_alert=True)
    elif data.startswith("NEXT"):
        if data.split(';')[1] == "CORRECT":
            markup = only_correct_markup
        else:
            markup = only_incorrect_markup

        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.id,
            reply_markup=markup
        )

        train_command_step_1(call)
    elif data == "RESET":
        reset_all_levels_of_memory(call.from_user.id)
        bot.answer_callback_query(callback_query_id=call.id, text="Теперб Вы снова можете упражняться по своим словам 😃", show_alert=True)