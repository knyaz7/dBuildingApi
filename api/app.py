from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка подключения к базе данных MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/dbuild'

db = SQLAlchemy(app)

# Модель данных для таблицы users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)  
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), unique=False)

    def __init__(self, login, email, password):  
        self.login = login
        self.email = email 
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.login  

class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    theme_name = db.Column(db.String(200), unique=False)
    rating = db.Column(db.Integer)

    def __init__(self, user_id, theme_name, rating):  
        self.user_id = user_id
        self.theme_name = theme_name 
        self.rating = rating

    def __repr__(self):
        return '<User %r>' % self.theme_name  

with app.app_context():
    db.create_all()

# Роут для получения всех пользователей
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {'id': user.id, 'login' : user.login, 'email': user.email, 'password': user.password}
        output.append(user_data)
    return jsonify(output)

# Роут для получения одного пользователя
@app.route('/api/users/<int:item_id>', methods=['GET'])
def get_user(item_id):
    user = User.query.get(item_id)
    if user:
        user_data = {'id': user.id, 'login': user.login, 'email': user.email, 'password': user.password}
        return jsonify(user_data)
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
