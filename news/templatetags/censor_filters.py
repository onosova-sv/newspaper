from django import template
import re

register = template.Library()

# Список нецензурных слов
BAD_WORDS = ["хрен", "ахрененно", "жопа"]

@register.filter(name='censor')

def censor(text):
    words = text.split()
    result = []
    for word in words:
        if word in BAD_WORDS:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)