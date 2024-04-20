from database import db

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    status = db.Column(db.Boolean, unique=False)

    def __init__(self, user_id, status):  
        self.user_id = user_id
        self.status = status

    def __repr__(self):
        return '<User %r>' % self.user_id  