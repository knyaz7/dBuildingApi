from database import db

class CurrencyExchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    summ = db.Column(db.Float, unique=False)
    currency_user = db.Column(db.String(50), unique=False)
    currency_bank = db.Column(db.String(50), unique=False)


    def __init__(self, application_id, summ, currency_user, currency_bank):
        self.application_id = application_id
        self.summ = summ
        self.currency_user = currency_user
        self.currency_bank = currency_bank


    def __repr__(self):
        return '<CurrencyExchange %r>' % self.title