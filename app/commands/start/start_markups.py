from telebot.types import ReplyKeyboardMarkup, KeyboardButton

greeting_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
greeting_markup.row(
    KeyboardButton("Тренировка 🎮"),
)

greeting_markup.row(
    KeyboardButton("Добавить слово ➕"),
    KeyboardButton("Удалить слово ➖"),
)

greeting_markup.row(
    KeyboardButton("Статистика 📈")
)