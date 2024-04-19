from flask import Flask
from Models.User import db as user_db
#from Models.Theme import db as theme_db
from Controllers.UserController import *

app = Flask(__name__)

# Настройка подключения к базе данных MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/dbuild'

user_db.init_app(app)
#theme_db.init_app(app)

with app.app_context():
    user_db.create_all()
    #theme_db.create_all()

# Роуты пользователя
app.route('/api/users/', methods=['GET'])(get_users)
app.route('/api/users/<int:item_id>', methods=['GET'])(get_user)
app.route('/api/users/', methods=['POST'])(add_user)
app.route('/api/users/<int:item_id>', methods=['PUT'])(update_user)

if __name__ == '__main__':
    app.run(debug=True)
