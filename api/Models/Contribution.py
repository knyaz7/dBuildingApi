from database import db

class Contribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    summ = db.Column(db.Float, unique=False)
    period = db.Column(db.Integer, unique=False)

    def __init__(self, application_id,summ, period):
        self.application_id = application_id
        self.summ = summ
        self.period = period

    def __repr__(self):
        return '<Contribution %r>' % self.title