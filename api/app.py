from flask import Flask
from database import db
from Models.User import User
from Models.Theme import Theme
from Controllers.UserController import *
from Controllers.ThemeController import *

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

if __name__ == '__main__':
    app.run(debug=True)
