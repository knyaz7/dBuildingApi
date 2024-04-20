from flask import Flask
from database import db
from Controllers.UserController import *
from Controllers.ThemeController import *
from Controllers.MessageController import *
from Controllers.ApplicationController import *
from Controllers.AutoCreditController import *


app = Flask(__name__)

# Настройка подключения к базе данных MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/dbuild'

db.init_app(app)

with app.app_context():
    db.create_all()

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

if __name__ == '__main__':
    app.run(debug=True)
