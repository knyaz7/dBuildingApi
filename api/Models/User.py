from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)  
    first_name = db.Column(db.String(50), unique=True)
    last_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), unique=False)

    def __init__(self, login, first_name, last_name, password):  
        self.login = login
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.login  