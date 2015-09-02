__author__ = 'arthur'

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Bank(db.Model):
    """Represents Bank entity."""
    id = db.Column(db.Integer, primary_key=True)
    uri_logo = db.Column(db.String(250), unique=True)
    name_am = db.Column(db.String(50), unique=True)
    name_ru = db.Column(db.String(50), unique=True)
    name_en = db.Column(db.String(50), unique=True)
    update_time = db.Column(db.DateTime, nullable=False)
    # One-to-Many relationship
    rates = db.relationship('Rate', backref='bank', lazy='dynamic')

    def __init__(self, uri_logo, update_time):
        self.uri_logo = uri_logo
        self.update_time = update_time

    def __unicode__(self):
        return self.name_en

    def __repr__(self):
        return unicode(self).encode('utf-8')

    def __str__(self):
        return unicode(self).encode('utf-8')


class Rate(db.Model):
    """Represents the Rates of the bank."""
    id = db.Column(db.Integer, primary_key=True)
    update_time = db.Column(db.DateTime, nullable=False)
    declared_update_time = db.Column(db.DateTime, nullable=False)
    usd_buying = db.Column(db.Numeric, nullable=False)
    usd_selling = db.Column(db.Numeric, nullable=False)
    eur_buying = db.Column(db.Numeric, nullable=False)
    eur_selling = db.Column(db.Numeric, nullable=False)
    # Foreign key
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'))

    def __init__(self, update_time):
        self.update_time = update_time

    def __unicode__(self):
        return self.update_time.strftime('%d/%m/%Y %H:%M:%S') + ' - ' + \
            'USD[' + '{:.2f}'.format(self.usd_buying) + ": " + '{:.2f}'.format(self.usd_selling) + ']; ' + \
            'EUR[' + '{:.2f}'.format(self.eur_buying) + ": " + '{:.2f}'.format(self.eur_selling) + ']'

    def __repr__(self):
        return unicode(self).encode('utf-8')

    def __str__(self):
        return unicode(self).encode('utf-8')