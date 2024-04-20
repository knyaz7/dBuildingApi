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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Условия договора:"/n + "Срок договора - 36 месяцев"/n)


