from database import db

class ConsumerCredit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False) 
    summ = db.Column(db.Float, unique=False)
    point = db.Column(db.String(100), unique=False)
    period = db.Column(db.Integer, unique=False)
    title = db.Column(db.String(64), unique=False)
    inn = db.Column(db.String(64), unique=False)
    fact_adress = db.Column(db.String(64), unique=False)
    avg_earning = db.Column(db.Float, unique=False)

    def __init__(self, application_id, summ, point, period, title, inn, fact_adress, avg_earning):  
        self.application_id = application_id
        self.summ = summ
        self.point = point
        self.period = period
        self.title = title
        self.inn = inn
        self.fact_adress = fact_adress
        self.avg_earning = avg_earning

    def __repr__(self):
        return '<ConsumerCredit %r>' % self.title  