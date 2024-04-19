from database import db

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
        return '<Theme %r>' % self.theme_name
