from database import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'), nullable=False)
    message = db.Column(db.String(2048), unique=False)
    time = db.Column(db.DateTime, unique=False)
    type = db.Column(db.Boolean) # 0 - text, 1 - audio
    code = db.Column(db.String(4), unique=False)
    sender = db.Column(db.Boolean) # 0 - user, 1 - server


    def __init__(self, theme_id, message, time, type, code, sender):  
        self.theme_id = theme_id
        self.message = message 
        self.time = time
        self.type = type
        self.code = code 
        self.sender = sender

    def __repr__(self):
        return '<Theme %r>' % self.message
