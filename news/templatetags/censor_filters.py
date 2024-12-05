from django import template
import re

register = template.Library()

# Список нецензурных слов
BAD_WORDS = ["хрен", "ахрененно", "жопа"]

@register.filter(name='censor')
def censor(text):
    """Заменяет нецензурные слова на звездочки (*)"""
    if not isinstance(text, str):
        return text

    # Создание регулярного выражения
    bad_words_regex = re.compile(r'\b(?:' + '|'.join(re.escape(word) for word in BAD_WORDS) + r')\b', re.IGNORECASE)

    # Замена обнаруженных нецензурных слов на звездочки
    return bad_words_regex.sub(lambda x: '*' * len(x.group()), text)