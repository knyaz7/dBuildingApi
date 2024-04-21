from database import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    input_wallet = db.Column(db.String(50), unique=False)
    output_wallet = db.Column(db.String(50), unique=False)
    summ = db.Column(db.Float, unique=False)


    def __init__(self, application_id, input_wallet, output_wallet, summ):
        self.application_id = application_id
        self.input_wallet = input_wallet
        self.output_wallet = output_wallet
        self.summ = summ


    def __repr__(self):
        return '<Transaction %r>' % self.title