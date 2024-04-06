from enum import Enum


class Roles(str, Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'


class Modes(str, Enum):
    CONTINUE = 'continue'
    END = 'end'


users_info = {}

users_state = {}

CHARS = ['Райан Гослинг', 'Альберт Эйнштейн', 'Илон Маск', 'Шрек']
GENRES = ['Юмор', 'Сенен', 'Романтика']
SETTINGS = ['Рядом с шаурмечной', 'Исекай', 'Школа']

USERS_STATES_TEXT = ['char', 'genre', 'setting']

CONTENT = {
    'char': {
        'text': 'Выбери персонажа!',
        'buttons_text': CHARS
    },
    'genre': {
        'text': 'Выбери жанр!',
        'buttons_text': GENRES
    },
    'setting': {
        'text': 'Выбери сеттинг',
        'buttons_text': SETTINGS
    }
}

CONTINUE_STORY = 'Продолжи сюжет в 1-3 предложения и оставь интригу. Не пиши никакой пояснительный текст от себя'
END_STORY = 'Напиши завершение истории c неожиданной развязкой. Не пиши никакой пояснительный текст от себя'

SYSTEM_PROMPT = (
    "Ты пишешь историю вместе с человеком. "
    "Историю вы пишете по очереди. Начинает человек, а ты продолжаешь. "
    "Если это уместно, ты можешь добавлять в историю диалог между персонажами. "
    "Диалоги пиши с новой строки и отделяй тире. "
    "Не пиши никакого пояснительного текста в начале, а просто логично продолжай историю"
)
