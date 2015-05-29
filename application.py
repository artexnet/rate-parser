__author__ = 'arthur'

import time
import logging
import schedule

from threading import Thread
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from config import *
from web.views import pages
from web.service import api
from web.error_handlers import *
from web.resources import rs


# Flask application initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.register_blueprint(pages)
app.register_blueprint(api)
app.register_blueprint(rs)
app.register_error_handler(400, bad_request)
app.register_error_handler(401, unauthorized)
app.register_error_handler(404, not_found)
app.register_error_handler(500, internal_server_error)
app.register_error_handler(501, not_implemented)


# Database initialization
db = SQLAlchemy(app)
from models import *
db.create_all()


# Parser initialization
from parsers import Parser
parser = Parser()
counter = 0


# Scheduled job
def run_schedule():
    global counter
    while 1:
        schedule.run_pending()
        if counter < parser.number_of_requests:
            # acquiring banks and rates data
            banks = parser.banks
            rates = parser.rates

            # saving data into DB
            for logo, bank in banks.iteritems():
                saved_bank = Bank.query.filter_by(uri_logo=bank.uri_logo).first()
                rate = rates[logo]

                if saved_bank:
                    saved_bank.update_time = bank.update_time
                    rate.bank_id = saved_bank.id
                else:
                    db.session.add(bank)
                    rate.bank = bank

                db.session.add(rate)
                try:
                    db.session.commit()
                except SQLAlchemyError as e:
                    app.logger.error(e.message, e)

            # increasing counter
            counter += 1
        time.sleep(1)


# Main
if __name__ == '__main__':
    schedule.every(PARSING_INTERVAL_SECONDS).seconds.do(parser.get_rates)
    t = Thread(target=run_schedule)
    t.start()

    # configuring application logger
    handler = RotatingFileHandler(APPLICATION_LOG_FILE, maxBytes=10000, backupCount=2)
    handler.setLevel(logging.INFO)
    handler.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app.logger.addHandler(handler)

    # running parser on first start
    if Rate.query.all().__len__() == 0:
        parser.get_rates()

    # starting Flask application
    app.run(debug=True, use_reloader=False)