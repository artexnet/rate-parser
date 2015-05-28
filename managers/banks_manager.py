__author__ = 'arthur'

from models import db, Bank, Rate
from sqlalchemy import and_

from helpers.query_helper import get_last_update_time_as_query
from helpers.query_helper import get_usd_selling_min_rate_as_query
from helpers.query_helper import get_eur_selling_min_rate_as_query
from helpers.query_helper import get_usd_buying_max_rate_as_query
from helpers.query_helper import get_eur_buying_max_rate_as_query


def get_banks():
    """Gets all stored banks."""
    return Bank.query.all()


def get_bank(bank_id):
    """Gets all stored banks."""
    return Bank.query.filter_by(id=bank_id).first()


def get_banks_count():
    """Gets number of banks in DB."""
    return db.session.query(Bank).count()


def get_usd_selling_best_rate_banks():
    """Gets banks with best USD selling rate."""
    return db.session\
        .query(Rate)\
        .join(Bank, Rate.bank_id == Bank.id)\
        .filter(
            and_(Rate.update_time == get_last_update_time_as_query(),
                 Rate.usd_selling == get_usd_selling_min_rate_as_query())
        ).all()


def get_eur_selling_best_rate_banks():
    """Gets banks with best EUR selling rate."""
    return db.session\
        .query(Rate)\
        .join(Bank, Rate.bank_id == Bank.id)\
        .filter(
            and_(Rate.update_time == get_last_update_time_as_query(),
                 Rate.eur_selling == get_eur_selling_min_rate_as_query())
        ).all()


def get_usd_buying_best_rate_banks():
    """Gets banks with best USD buying rate."""
    return db.session\
        .query(Rate)\
        .join(Bank, Rate.bank_id == Bank.id)\
        .filter(
            and_(Rate.update_time == get_last_update_time_as_query(),
                 Rate.usd_buying == get_usd_buying_max_rate_as_query())
        ).all()


def get_eur_buying_best_rate_banks():
    """Gets banks with best EUR buying rate."""
    return db.session\
        .query(Rate)\
        .join(Bank, Rate.bank_id == Bank.id)\
        .filter(
            and_(Rate.update_time == get_last_update_time_as_query(),
                 Rate.eur_buying == get_eur_buying_max_rate_as_query())
        ).all()