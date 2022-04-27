from flask import Flask, request
import logging
import json

from parser import Parser

modes = {
    "start": 1,
    "read_poem": 2,
    "learn_poem": 3,
    "qizz": 4,
    "change_mode": 5,
    "change_poem": 6,
    "change_poem_learn": 7
}
mode = modes["start"]

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


def created_response(version, session, text, end=False):
    response = {
        "version": version,
        "session": session,
        "response": {
            "end_session": end,
            "text": text
        }
    }
    return response

def mode_start(req):
    global mode
    end = False

    if req["request"]["original_utterance"].lower() in ['да', 'конечно', "ну давай", "давай"]:
        text = 'tutotial'
    elif req["request"]["original_utterance"].lower() in ['нет', 'не надо', "не зачем"]:
        mode = modes["change_mode"]
        text = "Что мы будем делать сегодня? Читать или учить стих? А может опробуем нашу новую ф-ию викторины?"
    else:
        text = "Мы к сожалению не поняли что вы хотели сказать."

    response = created_response(request.json["version"], request.json["session"], text, end)
    return json.dumps(response)


def mode_change(req):
    global mode
    end = False

    if req["request"]["original_utterance"].lower() in ['читать', 'читать стихи', 'читать стих']:
        text = 'Супер! Какое стихотворение будем читать?'
        mode = modes["change_poem"]
    elif req["request"]["original_utterance"].lower() in ['учить', 'учить стихи', "учить стих"]:
        text = 'Какое стихотворение вы бы хотели выучить? Назовите автора и название стих-я.'
        mode = modes["change_poem_learn"]
    elif req["request"]["original_utterance"].lower() in ['викторина', 'викторину']:
        text = 'tutorial. Начнём или стоит ещё раз объяснить?'
        mode = modes["learn_poem"]
    else:
        text = "Мы к сожалению не поняли что вы хотели сказать."

    response = created_response(request.json["version"], request.json["session"], text, end)
    return json.dumps(response)


def change_poem(req):
    global mode
    end = False
    result = req["request"]["original_utterance"].lower()
    text1 = Parser(result)
    text = (text1.verse())
    response = created_response(request.json["version"], request.json["session"], text, end)
    return json.dumps(response)



@app.route("/", methods=["POST"])
def main():
    global mode
    logging.info(request.json)
    end = False
    req = request.json
    if req["session"]["new"]:
        text = "Рада приветствовать Вас снова! Напомнить, что я умею?"
        response = created_response(request.json["version"], request.json["session"], text, end)
        return json.dumps(response)
    elif req["request"]["original_utterance"].lower() in ['выход', 'выключись']:
        end = True
        text = 'Пока брат'
        response = created_response(request.json["version"], request.json["session"], text, end)
        return json.dumps(response)
    else:
        if mode == modes["start"]:
            return mode_start(req)

        if mode == modes["change_mode"]:
            return mode_change(req)

        if mode == modes["change_poem"]:
            return change_poem(req)




