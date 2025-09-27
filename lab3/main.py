from sender import Sender
from receiver import Receiver
import json


# Вариант
# В, Б, Г, А, В
# Почтовый сервис: Yandex Mail (через SMTP/IMAP)
# Тип отправляемого сообщения: HTML-письмо с форматированием
# Источник данных для отправки: Генерация случайных тестовых данных
# Обработка входящей почты: Поиск писем с определенной темой
# Действие с найденными письмами: Скачать вложения в указанную папку


def load_config(filename = "conf.json") -> dict:
    with open(filename, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

def send_message(config):
    sender = Sender(config)
    sender.connect()
    sender.send()
    sender.disconnect()

def receive_message(config):
    receiver = Receiver(config)
    receiver.process_emails_with_attachments()
    receiver.disconnect()

def main():

    config = load_config()
    send_message(config)
    receive_message(config)

if __name__ == "__main__":
    main()