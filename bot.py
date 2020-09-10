import requests
from bottle import (
    run, post, response, request as bottle_request
)
from secret_token import token

BOT_URL = f'https://api.telegram.org/bot{token}/'


def get_chat_id(data):
    """Метод извлечения chat_id из запроса telegram бота"""
    chat_id = data['message']['chat']['id']

    return chat_id


def get_message(data):
    """Метод извлечения message_id из запроса telegram бота"""
    message_text = data['message']['text']

    return message_text


def send_message(prepared_data):
    """Подготовленные данные должны быть в формате json, которые включают как минимум chat_id и text."""
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)


def change_text_message(text):
    """Метод переворота текста сообщения"""
    return text[::-1]


def prepare_data_for_answer(data):
    answer = change_text_message(get_message(data))

    json_data = {
        "chat_id": get_chat_id(data),
        "text": answer,
    }

    return json_data


@post('/')
def main():
    data = bottle_request.json

    answer_data = prepare_data_for_answer(data)
    send_message(answer_data)
    return response  # status 200 OK по умолчанию


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
