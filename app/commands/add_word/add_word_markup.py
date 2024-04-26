from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_choose_word_markup(russian_word: str, owner_word: str, bot_word: str) -> InlineKeyboardMarkup:
    choose_word_markup = InlineKeyboardMarkup(row_width=1)
    choose_word_markup.add(
        InlineKeyboardButton("Оставить мой перевод", callback_data=f"USE_MY_TRANSLATING;{russian_word};{owner_word}"),
        InlineKeyboardButton("Использовать перевод бота", callback_data=f"USE_BOT_TRANSLATING;{russian_word};{bot_word}")
    )

    return choose_word_markup


confrimed_markup = InlineKeyboardMarkup(row_width=1)
confrimed_markup.add(
    InlineKeyboardButton("Слово добавлено ✔️", callback_data="CONFIRMED")
)