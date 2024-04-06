from enum import Enum
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup
from content import users_choices, users_state, USERS_STATES_TEXT, CONTENT
from gpt import create_system_prompt, count_tokens_in_text, get_gpt_answer
from config import TG_TOKEN, MAX_TOKENS_IN_SESSION
from db import create_db, create_table, insert_row, count_tokens_for_user_in_session, get_all_unique_messages_in_session

bot = TeleBot(TG_TOKEN)


class Roles(str, Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'


session_id = 0


def check_user_choices_created(message: Message):
    return users_choices.get(message.chat.id)


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
    cur_content = CONTENT[cur_user_state_text]
    buttons_text = cur_content['buttons_text']

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
        bot.send_message(message.chat.id, 'Круто, пиши запрос нейросети или введи команду /additional, '
                                          'чтобы добавить дополнительную информацию')
        return

    cur_user_state_text = get_text_state(cur_user_state_num)
    cur_content = CONTENT[cur_user_state_text]

    message_text = cur_content['text']
    buttons_text = cur_content['buttons_text']

    bot.send_message(message.chat.id, message_text,
                     reply_markup=create_keyboard(buttons_text))
    bot.register_next_step_handler(message, process_choice)


@bot.message_handler(commands=['additional'], func=check_user_choices_created)
def additional_handler(message: Message):
    bot.send_message(message.chat.id, 'Вводи доп инфу!')
    bot.register_next_step_handler(message, process_additional)


def process_additional(message: Message):
    users_choices[message.chat.id]['additional'] = message.text
    bot.send_message(message.chat.id, 'Принято!')


@bot.message_handler(content_types=['text'], func=check_user_choices_created)
def ask_gpt(message: Message):
    system_prompt = create_system_prompt(message.chat.id)
    system_tokens = count_tokens_in_text(system_prompt)

    insert_row((message.chat.id, Roles.SYSTEM, system_prompt, system_tokens, session_id))

    user_tokens = count_tokens_in_text(message.text)

    insert_row((message.chat.id, Roles.USER, message.text, user_tokens, session_id))

    tokens = count_tokens_for_user_in_session(message.chat.id, session_id)
    if tokens >= MAX_TOKENS_IN_SESSION:
        bot.send_message(message.chat.id, 'ТУ МАЧ')
        return
    user_history = get_all_unique_messages_in_session(message.chat.id, session_id)

    gpt_answer = get_gpt_answer(user_history)

    bot.send_message(message.chat.id, gpt_answer)


@bot.message_handler(content_types=['text'])
@bot.message_handler(commands=['help'])
def help_handler(message: Message):
    bot.send_message(message.chat.id, 'Введи /new_story чтобы начать')


create_db()
create_table()

bot.polling()
