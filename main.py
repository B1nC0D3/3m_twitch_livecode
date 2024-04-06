import requests

from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup
from config import TG_TOKEN


bot = TeleBot(TG_TOKEN)

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

users_choices = {}

users_state = {}


def get_text_state(cur_state_num):
    return USERS_STATES_TEXT[cur_state_num]


def create_keyboard(text_buttons):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    markup.add(*text_buttons)
    return markup


@bot.message_handler(commands=['start'])
def start_handler(message: Message):
    bot.send_message(message.chat.id, 'hello!')


@bot.message_handler(commands=['new_story'])
def new_story_handler(message: Message):
    users_choices[message.chat.id] = {}
    user_state_num = users_state[message.chat.id] = 0
    user_state = get_text_state(user_state_num)

    markup = create_keyboard(CONTENT[user_state]['buttons_text'])

    bot.send_message(message.chat.id,
                     'Ты начал новую историю.')
    bot.send_message(message.chat.id,
                     CONTENT[user_state]['text'],
                     reply_markup=markup)
    bot.register_next_step_handler(message, process_choice)


def process_choice(message: Message):
    cur_user_state_num = users_state[message.chat.id]
    cur_user_state_text = get_text_state(cur_user_state_num)
    cur_user_state = CONTENT[cur_user_state_text]
    buttons_text = cur_user_state['buttons_text']

    if message.text not in buttons_text:
        bot.send_message(message.chat.id,
                         'Нажимай на кнопочки!',
                         reply_markup=create_keyboard(buttons_text))
        bot.register_next_step_handler(message, process_choice)
        return

    users_choices[message.chat.id][cur_user_state_text] = message.text

    users_state[message.chat.id] += 1
    cur_user_state_num += 1

    if cur_user_state_num >= len(USERS_STATES_TEXT):
        bot.send_message(message.chat.id, 'Круто, пиши запрос нейросети!')
        bot.register_next_step_handler(message, ask_gpt)
        return

    cur_user_state_text = get_text_state(cur_user_state_num)
    cur_user_state = CONTENT[cur_user_state_text]

    message_text = cur_user_state['text']
    buttons_text = cur_user_state['buttons_text']

    bot.send_message(message.chat.id, message_text,
                     reply_markup=create_keyboard(buttons_text))
    bot.register_next_step_handler(message, process_choice)


def ask_gpt(message):
    print(users_choices)


bot.polling()
