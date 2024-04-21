from flask import Flask, request, send_file
from flask_cors import CORS
from database import db
from Controllers.UserController import *
from Controllers.ThemeController import *
from Controllers.MessageController import *
from Controllers.ApplicationController import *
from Controllers.AutoCreditController import *
from Controllers.ConsumerCreditController import *
from Controllers.MortgageController import *
from Controllers.CurrencyExchangeController import *
from Controllers.ContributionController import *
import pyttsx3
import os

app = Flask(__name__)
CORS(app) # Включаем поддержку CORS для всего приложения

# Настройка подключения к базе данных MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/dbuild'

db.init_app(app)

with app.app_context():
    db.create_all()

def text_to_audio(text, path):
    engine = pyttsx3.init()
    engine.save_to_file(text, path)
    engine.runAndWait()

def convert_text_to_audio():
    if os.path.exists('output_audio.wav'):
        os.remove('output_audio.wav')
    if 'text' not in request.form:
        return jsonify({'error': 'Text parameter is missing'}), 400

    text = request.form['text']

    # Уникальное имя для аудиофайла
    audio_file_path = 'output_audio.wav'

    # Преобразование текста в аудиофайл
    text_to_audio(text, audio_file_path)

    # Посылаем аудиофайл обратно в ответе
    return send_file(audio_file_path, as_attachment=True)

# Роуты пользователя
app.route('/api/users/', methods=['GET'])(get_users)
app.route('/api/users/<int:item_id>', methods=['GET'])(get_user)
app.route('/api/users/', methods=['POST'])(add_user)
app.route('/api/users/<int:item_id>', methods=['PUT'])(update_user)

# Роуты темы
app.route('/api/themes/', methods=['GET'])(get_themes)
app.route('/api/themes/<int:item_id>', methods=['GET'])(get_theme)
app.route('/api/themes/', methods=['POST'])(add_theme)
app.route('/api/themes/<int:item_id>', methods=['PUT'])(update_theme)

# Роуты сообщений
app.route('/api/messages/', methods=['GET'])(get_messages)
app.route('/api/messages/<int:item_id>', methods=['GET'])(get_message)
app.route('/api/messages/', methods=['POST'])(add_message)

# Роуты заявок
app.route('/api/applications/', methods=['GET'])(get_applications)
app.route('/api/applications/<int:item_id>', methods=['GET'])(get_application)
app.route('/api/applications/', methods=['POST'])(add_application)
app.route('/api/applications/<int:item_id>', methods=['PUT'])(update_application)

# Роуты автокредитов
app.route('/api/autocredits/', methods=['GET'])(get_autocredits)
app.route('/api/autocredits/<int:item_id>', methods=['GET'])(get_autocredit)
app.route('/api/autocredits/', methods=['POST'])(add_autocredit)
app.route('/api/autocredits/<int:item_id>', methods=['PUT'])(update_autocredit)

# Роуты потребительских кредитов
app.route('/api/consumercredits/', methods=['GET'])(get_consumercredits)
app.route('/api/consumercredits/<int:item_id>', methods=['GET'])(get_consumercredit)
app.route('/api/consumercredits/', methods=['POST'])(add_consumercredit)
app.route('/api/consumercredits/<int:item_id>', methods=['PUT'])(update_consumercredit)

# Роуты потребительских кредитов
app.route('/api/mortgages/', methods=['GET'])(get_mortgages)
app.route('/api/mortgages/<int:item_id>', methods=['GET'])(get_mortgage)
app.route('/api/mortgages/', methods=['POST'])(add_mortgage)
app.route('/api/mortgages/<int:item_id>', methods=['PUT'])(update_mortgage)

# Роуты обмена валюты
app.route('/api/currencyexchanges/', methods=['GET'])(get_currencyexchanges)
app.route('/api/currencyexchanges/<int:item_id>', methods=['GET'])(get_currencyexchange)
app.route('/api/currencyexchanges/', methods=['POST'])(add_currencyexchange)
app.route('/api/currencyexchanges/<int:item_id>', methods=['PUT'])(update_currencyexchange)

# Роуты вклада
app.route('/api/contributions/', methods=['GET'])(get_contributions)
app.route('/api/contributions/<int:item_id>', methods=['GET'])(get_contribution)
app.route('/api/contributions/', methods=['POST'])(add_contribution)
app.route('/api/contributions/<int:item_id>', methods=['PUT'])(update_contribution)

app.route('/api/converttexttoaudio/', methods=['POST'])(convert_text_to_audio)

if __name__ == '__main__':
    app.run(debug=True)