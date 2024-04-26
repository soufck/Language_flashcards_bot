from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_train_markup(russian_word: str) -> InlineKeyboardMarkup:
    train_markup = InlineKeyboardMarkup(row_width=2)
    train_markup.add(
        InlineKeyboardButton("✅", callback_data=f"CORRECT;{russian_word}"),
        InlineKeyboardButton("❌", callback_data=f"INCORRECT;{russian_word}")
    )

    return train_markup


only_correct_markup = InlineKeyboardMarkup(row_width=1)
only_correct_markup.add(
    InlineKeyboardButton("✅", callback_data="+"),
    InlineKeyboardButton("Дальше ➡️", callback_data="NEXT")
)


only_incorrect_markup = InlineKeyboardMarkup(row_width=1)
only_incorrect_markup.add(
    InlineKeyboardButton("❌", callback_data="-"),
    InlineKeyboardButton("Дальше ➡️", callback_data="NEXT")
)


reset_markup = InlineKeyboardMarkup(row_width=1)
reset_markup.add(
    InlineKeyboardButton("Сбросить 🔄", callback_data="RESET"),
)
