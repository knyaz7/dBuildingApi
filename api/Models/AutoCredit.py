from database import db

class AutoCredit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False) 
    car_price = db.Column(db.Float, unique=False)
    first_payment = db.Column(db.Float, unique=False)
    period = db.Column(db.Integer, unique=False)
    title = db.Column(db.String(64), unique=False)
    inn = db.Column(db.String(64), unique=False)
    fact_adress = db.Column(db.String(64), unique=False)
    avg_earning = db.Column(db.Float, unique=False)

    def __init__(self, application_id, car_price, first_payment, period, title, inn, fact_adress, avg_earning):  
        self.application_id = application_id
        self.car_price = car_price
        self.first_payment = first_payment
        self.period = period
        self.title = title
        self.inn = inn
        self.fact_adress = fact_adress
        self.avg_earning = avg_earning

    def __repr__(self):
        return '<User %r>' % self.user_id  