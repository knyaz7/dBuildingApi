import speech_recognition as sr
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
from g4f.client import Client
import re


def rating(theme_dialog):
    # Установка политики цикла событий для предотвращения предупреждения на Windows
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    # Инициализация клиента
    client = Client()

    # Отправка сообщения  и получение ответа
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": "Оцени по манере общения пользователя, его удовлетворенность диалогом по стобальной шкале. Ответ предоставь исключительно в численном виде. Диалог: " + theme_dialog}]
    )

    # Вывод ответа0,
    estimation = response.choices[0].message.content
    return estimation


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
def request_gpt(text, list_of_target_topics):
    # Установка политики цикла событий для предотвращения предупреждения на Windows
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    # Инициализация клиента
    client = Client()

    # Отправка сообщения и получение ответа
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": "Укажи тему обращения, если она есть в списке {" + ', '.join(list_of_target_topics) +"},то укажи из списка, в ином случае задай название темы самостоятельно, а затем предоставь ответ на обращение. Не забывай про точки в тексте. Формат: Тема:...  Ответ:... Обращение: " + text}]
    )

    # Вывод ответа0,
    return response.choices[0].message.content

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
        return response, theme
    else:
        return "none", "none"


def target_topics_check(theme):
    match theme:
        case "Открытие кредита":
            print("Какой кредит вы хотите открыть. Потребительский, Автокредит или Ипотека?")
            match response:
                case "Потребительский":
                    print("Какая у вас цель кредитования?")
                    print("На какую сумму вы хотите взять кредит?")
                    print("На какой срок вы планируете взять кредит?")
                case "Автокредит":
                    print("Какая стоимость автомобиля?")
                    print("Каков первоначальный взнос?")
                    print("На какой срок вы планируете взять кредит?")
                case "Ипотека":
                    print("Какая у вас цель кредитования?")
                    print("На какую сумму вы хотите взять кредит?")
                    print("Каков первоначальный взнос?")
                    print("На какой срок вы планируете взять кредит?")
            print("Укажите Наименование")
            print("Укажите ИНН")
            print("Укажите Фактический адрес компании по месту вашей работы")
            print("Укажите Среднемесячный доход после уплаты налогов за последние 12 месяцев")
            #   ПЕРЕКИДЫВАЕТ НА СТРАНИЦУ СОГЛАСОВАНИЯ ВВЕДЕННЫХ ДАННЫХ 

        case "Открытие вклада":
            print("Forbidden")
        case "Обмен валюты":
            print("Not Found")
        case "Перевод":
            print("Перевод")
        case "История операций":
            print("Перевод")
        case "Расход за период":
            print("Перевод")



if __name__ == '__main__':
    list_of_target_topics = ("Открытие кредита", "Открытие вклада", "Обмен валюты", "Перевод", "История операций", "Расход за период")
    text = "Открой кредитный счет"
    response = request_gpt(text, list_of_target_topics)
    response, theme = get_theme_and_response(response)
    print(response)
    print(theme)








