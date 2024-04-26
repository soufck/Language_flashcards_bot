choose_word_text = lambda russian, english, recommended:'\n'.join([
    f"Ваше слово на русском: {russian}",
    f"Ваше слово на английском: {english}",
    f"",
    f"<tg-spoiler>Рекомендованный ботом перевод: {recommended}</tg-spoiler>"
])