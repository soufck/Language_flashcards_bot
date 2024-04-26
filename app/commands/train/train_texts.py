def correct_checking_text(user_answer: str, foreign_word: str) -> str:
    return '\n'.join([
        f"<b>Приавльный ответ:</b> <code>{foreign_word}</code>",
        f"<b>Ваш ответ:</b> <code>{user_answer}</code>",
        f"",
        f"Вы ответили верно?"
    ]) 


def how_it_can_be_translated(russian_word: str) -> str:
    return '\n'.join([
        f"Как переводится слово <code>{russian_word}</code>?"
    ])