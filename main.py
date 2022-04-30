from flask import Flask, request
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


def created_response(version, session, text, value=False, end=False,) -> dict:
    """
    Created response for Alice

    :param version: version
    :param session: config session
    :param text: text for Alice
    :param value: value for safe storage
    :param end: True - end session, False - continue session
    :return: dict
    """
    response = {
        "version": version,
        "session": session,
        "response": {
            "end_session": end,
            "text": text
        },
        "session_state": {
            "value": value
        },
    }
    return response


@app.route("/", methods=["POST"])
def main():
    """
    req["session"]["new"] - checking for a new session
    req["request"]["original_utterance"] - user response
    req["state"]["session"]["value"] - 'safe storage' value (not working)

    :return: None
    """
    logging.info(request.json)
    end = False
    req = request.json  # request from Alice

    if req["session"]["new"]:   # session is new?
        text = "Рада приветствовать Вас снова! Напомнить, что я умею?"
        value = "start"

    elif req["request"]["original_utterance"].lower() in ['выход', 'выключись']:    # exit
        end = True
        text = 'Пока брат'

    elif req["state"]["session"]["value"] == "start":   # if mode start
        if req["request"]["original_utterance"].lower() in ['да', 'конечно', 'давай']:
            text = """1 Я могу прочитать Вам стих: достаточно сказать Алиса, прочти стихотворение
                    2 Я могу помочь выучить стих, скажите Алиса, давай выучим стихотворение
                    3 Так же Вы можете испытать свои знания в литературе, сказав Алиса, включи режим викторины"""
            value = "tutorial_start"

        if req["request"]["original_utterance"].lower() in ['нет', 'не надо']:
            text = """Что мы будем делать сегодня?
                        Читать или учить стих? А может опробуем нашу новую ф-ию викторины?"""
            value = "change_mode"

    elif req["state"]["session"]["value"] == "tutorial_start":
        text = """Что мы будем делать сегодня?
                Читать или учить стих? А может опробуем нашу новую ф-ию викторины?"""
        value = "change_mode"

    elif req["state"]["session"]["value"] == "change_mode":
        if req["request"]["original_utterance"].lower() in ['читать', 'читать стих', 'читать стихи']:
            text = """Супер!
                        Какое стихотворение будем читать?"""
            value = "change_author_title_read"

        if req["request"]["original_utterance"].lower() in ['учить', 'учить стих', 'учить стихи']:
            text = """Какое стихотворение вы бы хотели выучить? Назовите автора и название стих-я."""
            value = "change_author_title_learn"

    elif req["state"]["session"]["value"] == "change_author_title_read":
        text = f'Вы назвали {req["request"]["original_utterance"].lower()}'
        value = "read"

    elif req["state"]["session"]["value"] == "change_author_title_learn":
        text = f'Вы назвали {req["request"]["original_utterance"].lower()}'
        value = "learn"

    response = created_response(request.json["version"], request.json["session"], text, value=value)
    # created response for Alice
    return json.dumps(response)
