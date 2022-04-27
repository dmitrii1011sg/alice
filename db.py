import colorama
import pyrebase
from colorama import Back, Fore
from config import *

colorama.init()

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
data = db.child('poems').get().val()


def send_conclusion(msg: str, f: bool):  # Вспомогательная функция (скип)
    if f:
        print(Back.GREEN, Fore.BLACK + msg)
    else:
        print(Back.RED, Fore.BLACK + msg)


def db_push(current_data: dict):  # Вспомогательная функция (скип)
    db.child('poems').set(current_data)


def db_add_poem(author: str, title: str, content: str):  # Добавление стиха в каталог к уже соществующему автору
    if author in data.keys():
        if title.lower().capitalize() in data[author].keys():
            message = f'Стихотворение "{title}" У "{author}" уже существует'
            send_conclusion(message, False)
        else:
            data[author][title.lower().capitalize()] = content
            db_push(data)
            message = f'Стихотворение "{title}" добавлено в каталог к "{author}"'
            send_conclusion(message, True)
    else:
        message = f'Этого автора нет в базе'
        send_conclusion(message, False)


def db_add_poet(author: str):  # Добавление автора
    if author.lower().capitalize() in data.keys():
        message = f'{author} уже есть в базе данных'
        send_conclusion(message, False)
    else:
        data[author.lower().capitalize()] = {'sys': 0}
        db_push(data)
        message = f'{author} успешно добавлен в базу данных'
        send_conclusion(message, True)


def db_get_poem(author: str, title: str) -> str:  # Возвращает стихотворение
    if author in data.keys():
        if title.lower().capitalize() in data[author].keys():
            message = data[author][title.lower().capitalize()]
            return Fore.YELLOW + message
        else:
            message = f'Стихотворения "{title}" у "{author}" не найдено'
            send_conclusion(message, False)
    else:
        message = f'Этого автора нет в базе'
        send_conclusion(message, False)


def db_get_poet(author: str) -> dict:  # Возвращает все стихотворения автора
    if author.lower().capitalize() in data.keys():
        poems = dict()
        for key, value in data[author.lower().capitalize()].items():
            if key == 'sys': continue
            poems[key] = value
        return poems
    else:
        message = f'Этого автора нет в базе'
        send_conclusion(message, False)
        return {}


def db_get_poets() -> list:  # Возвращает список всех авторов
    poets = list()
    for i in data.keys():
        if i == 'sys': continue
        poets.append(i)
    return poets


def db_delete_poem(author: str, title: str):  # Удаляет стихотворение из каталога автора
    if author in data.keys():
        if title.lower().capitalize() in data[author].keys():
            data[author][title.lower().capitalize()] = {}
            db_push(data)
            message = f'Стихотворение "{title}" удалено у "{author}"'
            send_conclusion(message, True)
        else:
            message = f'Стихотворения "{title}" у "{author}" не найдено'
            send_conclusion(message, False)
    else:
        message = f'Этого автора нет в базе.'
        send_conclusion(message, False)


def db_delete_poet(author: str):  # Удаляет автора и все его стихи из базы данных
    if author.lower().capitalize() in data.keys():
        if input(Back.WHITE + f'Вы уверены что хотите удалить "{author}" и все его стихи? [Y/N]') == 'Y':
            db[author] = {}
            db_push(data)
            message = f'"{author}" успешно удален'
            send_conclusion(message, True)
        else:
            message = f'Действие отменено'
            send_conclusion(message, False)
    else:
        message = f'"{author}" нет в базе данных'
        send_conclusion(message, False)


print(db_get_poets())
