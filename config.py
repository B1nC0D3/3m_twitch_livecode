import os

from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
FOLDER_ID = os.getenv('FOLDER_ID')
GPT_TOKEN = os.getenv('GPT_TOKEN')

TOKENIZER_URL = 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize'
GPT_URL = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'

GPT_MODEL = 'yandexgpt-lite'
MAX_TOKENS_IN_SESSION = 1000000000000000
MAX_TOKENS_FOR_ANSWER = 200
HEADERS = {'Authorization': f'Bearer {GPT_TOKEN}'}
DEFAULT_DATA = {
    "modelUri": f"gpt://{FOLDER_ID}/{GPT_MODEL}/latest",
    "completionOptions": {
        "stream": False,
        "temperature": 0.7,
        "maxTokens": MAX_TOKENS_FOR_ANSWER
    },
}
