from flask import jsonify, request
from Models.Theme import Theme, db
from Models.Message import Message
from sqlalchemy import desc
from datetime import datetime
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
from g4f.client import Client
import re

def themeRating(theme_dialog_user):
    # Установка политики цикла событий для предотвращения предупреждения на Windows
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    # Инициализация клиента
    client = Client()

    # Отправка сообщения  и получение ответа
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": "Оцени по манере общения пользователя, его удовлетворенность диалогом по стобальной шкале. \
                    Ответ предоставь исключительно в численном виде, при оценке учитывай, что схожие сообщения, идущие подряд, уменьшают рейтинг. \
                        Сообщения пользователя: " + theme_dialog_user}]
    )

    # Вывод ответа
    estimation = response.choices[0].message.content
    
    if estimation.isnumeric():
        return int(estimation)
    else:
        return re.search(r'\d+', estimation).group()
    
def get_themes():
    themes = Theme.query.all()
    output = {
        'status': True if len(themes) > 0 else False,
        'message': "OK" if len(themes) > 0 else "Empty table",
        'data': []
    }
    for theme in themes:
        user_data = {'id': theme.id, 'user_id': theme.user_id, 'theme_name': theme.theme_name, 'rating': theme.rating}
        output['data'].append(user_data)
    return jsonify(output)

def get_theme(item_id):
    theme = Theme.query.get(item_id)
    if theme:
        user_data = {'id': theme.id, 'user_id': theme.user_id, 'theme_name': theme.theme_name, 'rating': theme.rating}
        return jsonify({'status': True, 'message': 'OK', 'data': user_data})
    else:
        return jsonify({'status': False, 'message': 'Theme not found'}), 404
    
def add_theme():
    user_id = request.form.get('user_id')
    theme_name = request.form.get('theme_name')

    if not user_id or not theme_name:
        return jsonify({'status': False, 'error': 'Missing required fields'}), 400

    rating = request.form.get('rating', -1)  # По умолчанию -1, если значение не передано

    new_theme = Theme(user_id=user_id, theme_name=theme_name, rating=rating)
    db.session.add(new_theme)
    db.session.commit()

    inserted_theme_id = new_theme.id

    previous_theme = Theme.query.filter(Theme.id != inserted_theme_id, Theme.user_id == user_id).order_by(desc(Theme.id)).first()

    if previous_theme:
        # Получаем все сообщения предыдущей темы, где sender=False
        previous_messages = Message.query.filter_by(theme_id=previous_theme.id, sender=False).all()

        # Формируем строку сообщений предыдущей темы
        previous_messages_text = " ".join([f"{i+1}) {message.message}" for i, message in enumerate(previous_messages)])

        # Получаем рейтинг с помощью функции themeRating
        rating = themeRating(previous_messages_text)

        # Обновляем рейтинг предыдущей темы
        previous_theme.rating = rating

        # Сохраняем изменения в базе данных
        db.session.commit()

    return jsonify({'status': True, 'message': 'Theme added successfully', 'theme_id': inserted_theme_id}), 201


def update_theme(item_id):
    theme = Theme.query.get(item_id)
    if not theme:
        return jsonify({'status': False, 'message': 'Theme not found'}), 404

    user_id = request.form.get('user_id')
    theme_name = request.form.get('theme_name')
    rating = request.form.get('rating')

    if user_id:
        theme.user_id = user_id
    if theme_name:
        theme.theme_name = theme_name
    if rating:
        theme.rating = rating

    db.session.commit()
    return jsonify({'status': True, 'message': 'Theme updated successfully'})
