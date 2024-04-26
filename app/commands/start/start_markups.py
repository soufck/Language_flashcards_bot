from telebot.types import ReplyKeyboardMarkup, KeyboardButton

greeting_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
greeting_markup.add(
    KeyboardButton("Тренировка 🎮"),
    KeyboardButton("Добавить слово ➕"),
    KeyboardButton("Статистика 📈")
)
