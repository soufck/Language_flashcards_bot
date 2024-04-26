def generate_human_statistic_text(dictionary: dict) -> str:
    return '\n'.join([
        f"🆔 - <code>{dictionary['telegram_id']}</code>",
        f"",
        f"<b>Всего слов:</b> {dictionary['total_count_of_words']} 📝",
        f"<b>Правильных ответов:</b> {dictionary['count_of_correctly_translated_words']} ✔️",
        f"<b>Неправильных оветов:</b> {dictionary['count_of_incorrectly_translated_words']} ✖️"
    ])