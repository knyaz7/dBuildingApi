from flask import jsonify, request
from Models.Message import Message, db
from Models.Theme import Theme
from sqlalchemy import desc
from datetime import datetime
import speech_recognition as sr
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
from g4f.client import Client
import re
import requests

def audio_to_text(audio):
    # Создаем объект распознавателя речи
    recognizer = sr.Recognizer()

    # Загружаем аудио файл
    audio_file = sr.AudioFile(audio)

    # Распознаем речь из аудио файла
    with audio_file as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="ru-RU")

    return text

def get_theme_and_response(text):
    text = re.sub(r'\n', '', text)
    # Паттерн для поиска темы и ответа
    pattern = r'Тема: (.+)Ответ: (.+)'

    # Поиск совпадений с помощью регулярного выражения
    match = re.search(pattern, text)

    # Если найдено совпадение, создаем переменные theme и response
    if match:
        theme = match.group(1)
        response = match.group(2)
        theme = re.sub(r'[^а-яёА-ЯЁ]', ' ', theme.lower())
        return response, theme
    else:
        return "none", "none"

def check_previous_theme(previous_theme, new_theme):

    # Установка политики цикла событий для предотвращения предупреждения на Windows
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    # Инициализация клиента
    client = Client()

    # Отправка сообщения и получение ответа
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": "Если эти подтемы имеют общую тему, напиши Да, в ином случае напиши Нет. Ответ должен быть строго только Да или Нет. \
                    Подтема 1:" + previous_theme +" . Подтема 2: " + new_theme 
                }] 
    )

    if response.choices[0].message.content == "Да":
        return previous_theme
    else:
        return new_theme

def request_gpt(text, list_of_target_topics, previous_theme, previous_theme_id):
    # Установка политики цикла событий для предотвращения предупреждения на Windows
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    # Инициализация клиента
    client = Client()

    # Отправка сообщения и получение ответа
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": "Ты голосовой помощник банка. Укажи тему обращения, если она есть в списке {" + ', '.join(list_of_target_topics) +"},то укажи из списка, в ином случае задай название темы самостоятельно, а затем предоставь ответ на обращение. Не забывай про точки в тексте. Формат: Тема:...  Ответ:... Обращение: " + text + ". Отвечай в строго указанном формате."}],

    )
    response, theme = get_theme_and_response(response.choices[0].message.content)
    if check_previous_theme(previous_theme, theme) == previous_theme:
        # ПОЛУЧИТЬ ВЕСЬ СПИСОК СООБЩЕНИЙ ПО ТЕМЕ previous_theme И ПРИСВОИТЬ ЭТО В TEXT (Сообщения в теме должны быть пронумерованны)
        # Получаем все сообщения по теме
        messages = Message.query.filter_by(theme_id=previous_theme_id).all()

        # Формируем текст с пронумерованными сообщениями
        newText = ""
        for i, message in enumerate(messages, start=1):
            newText += f"{i}) {message.message} "
            x = i + 1
        newText += f"{x}) {text}"

        # Установка политики цикла событий для предотвращения предупреждения на Windows
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

        # Инициализация клиента
        client = Client()

        # Отправка сообщения и получение ответа
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user",
                       "content": "Ответь на последнее обращение по номеру, учитывая остальной контекст. Дай только ответ. \
                        История диалога, где поочередно задается обращение и выдается ответ: " + newText}]
        )
        return response.choices[0].message.content, previous_theme
    else:
        return response, theme

def get_messages():
    messages = Message.query.all()
    output = {
        'status': True if len(messages) > 0 else False,
        'message': "OK" if len(messages) > 0 else "Empty table",
        'data': []
    }
    for message in messages:
        user_data = {'id': message.id, 'theme_id': message.theme_id, 'message': message.message, 'time': message.time, 'type': message.type, 'code': message.code, 'sender': message.sender}
        output['data'].append(user_data)
    return jsonify(output)

def get_message(item_id):
    message = Message.query.get(item_id)
    if message:
        user_data = {'id': message.id, 'theme_id': message.theme_id, 'message': message.message, 'time': message.time, 'type': message.type, 'code': message.code, 'sender': message.sender}
        return jsonify({'status': True, 'message': 'OK', 'data': user_data})
    else:
        return jsonify({'status': False, 'message': 'Message not found'}), 404
    
def add_message():
    user_id = request.form.get('user_id')
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    type = request.form.get('type')
    code = request.form.get('code')
    sender = False

    if not user_id or not type or not code:
        return jsonify({'status': False, 'message': 'Missing required fields'}), 400
    
    if type == '1':
        # Проверяем, есть ли файл в запросе
        if 'message' not in request.files:
            return jsonify({'status': False, 'message': 'No file part'}), 400

        # Получаем файл из запроса
        message_file = request.files['message']
        message = audio_to_text(message_file)
    else:
        message = request.form.get('message')
    
    # Находим последнюю тему для данного пользователя
    last_theme = Theme.query.filter_by(user_id=user_id).order_by(desc(Theme.id)).first()

    if last_theme is None:
        last_theme = "chupakabra"
        last_theme_id = 0
    else: 
        last_theme_id = last_theme.id
        last_theme = last_theme.theme_name

    response, theme = request_gpt(message, ("Открытие кредита", "Открытие вклада", "Обмен валюты", "Перевод", "История операций", "Расход за период"), last_theme, last_theme_id)
    if (response == "none"):
        response, theme = request_gpt(message, ("Открытие кредита", "Открытие вклада", "Обмен валюты", "Перевод", "История операций", "Расход за период"), last_theme, last_theme_id)

    # spec_theme = ("открытие кредита", "открытие вклада", "обмен валюты", "перевод", "история операций", "расход за период")
    # if theme.strip() in spec_theme:
    #     if theme == spec_theme[0]:
    #         code = "100"
    #     elif theme == spec_theme[1]:
    #         code = "200"
    #     elif theme == spec_theme[2]:
    #         code = "300"
    #     elif theme == spec_theme[3]:
    #         code = "400"
    #     elif theme == spec_theme[4]:
    #         code = "500"
    #     elif theme == spec_theme[5]:
    #         code = "600"

    if last_theme.strip() == theme.strip():
        theme_id = last_theme_id
    else:
        url = 'http://localhost:5000/api/themes/'
        payload = {
            'user_id': user_id,
            'theme_name': theme
        }
        themeJSON = requests.post(url, data=payload)
        # Обработка ответа и извлечение theme_id
        if themeJSON.status_code == 201:  # Проверяем успешность запроса
            theme_id = themeJSON.json().get('theme_id')

    new_message = Message(theme_id=theme_id, message=message, time=time, type=bool(int(type)), code=code, sender = sender)
    new_response = Message(theme_id=theme_id, message=response, time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), type=False, code=000, sender = True)
    db.session.add(new_message)
    db.session.add(new_response)
    db.session.commit()

    inserted_message_id = new_message.id

    return jsonify({'status': True, 'message': 'Message added successfully', 'message_id': inserted_message_id}), 201
