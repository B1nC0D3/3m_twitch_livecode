import requests
from pprint import pprint
from content import SYSTEM_PROMPT, users_choices
from config import DEFAULT_DATA, TOKENIZER_URL, HEADERS, GPT_URL


def get_gpt_answer(messages):
    data = DEFAULT_DATA.copy()
    data['messages'] = []
    for message in messages:
        role, content = message
        data['messages'].append(
            {'role': role,
             'text': content}
        )

    resp = send_request('post', GPT_URL, data)
    pprint(resp)
    return resp['result']['alternatives'][0]['message']['text']


def create_system_prompt(chat_id):
    user_choices = users_choices[chat_id]
    message = (f"\nНапиши начало истории в стиле {user_choices['genre']} "
               f"с главным героем {user_choices['char']}. "
               f"Вот начальный сеттинг: \n{user_choices['setting']}. \n"
               "Начало должно быть коротким, 1-3 предложения.\n")

    return SYSTEM_PROMPT + message


def send_request(method, url, data):
    resp = requests.request(method, url, json=data, headers=HEADERS)
    return resp.json()


def count_tokens_in_text(text):
    data = DEFAULT_DATA.copy()
    data['text'] = text
    response = send_request('post', TOKENIZER_URL, data)
    return len(response['tokens'])