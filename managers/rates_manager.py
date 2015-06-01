__author__ = 'arthur'

from models import db, Rate, Bank
from sqlalchemy import func, and_
from sqlalchemy.orm import aliased

from helpers.query_helper import get_last_update_time_as_query


def get_bank_latest_rates(bank_id):
    """Gets latest rates for selected bank."""
    r = aliased(Rate)
    max_dates = Rate.query.with_entities(func.max(r.update_time).label('maxdate')). \
        filter(and_(Rate.bank_id == r.bank_id, Rate.bank_id == bank_id))
    return Rate.query.filter_by(update_time=max_dates).first()


def get_bank_rates_from_date(bank_id, date_from):
    """Gets bank rates from provided date for the selected bank."""
    return Rate.query.join(Bank, Rate.bank_id == Bank.id). \
        filter(and_(Rate.bank_id == bank_id, Rate.update_time >= date_from)). \
        all()


def get_bank_rates_for_date_range(bank_id, date_from, date_to):
    """Gets bank rates within provided date range for the selected bank."""
    return Rate.query.join(Bank, Rate.bank_id == Bank.id). \
        filter(and_(Rate.bank_id == bank_id, Rate.update_time >= date_from, Rate.update_time <= date_to)). \
        all()


def get_average_rates():
    """Gets average rates for all period."""
    sub = Rate.query\
        .group_by('bank_id')\
        .order_by('update_time desc')\
        .subquery()

    return db.session.query(sub.c.update_time,
                            func.avg(sub.c.usd_buying),
                            func.avg(sub.c.usd_selling),
                            func.avg(sub.c.eur_buying),
                            func.avg(sub.c.eur_selling)).one()


def get_average_rates_from_date(date_from):
    """Gets average rates counted from selected date."""
    sub = Rate.query\
        .group_by('bank_id')\
        .filter(Rate.update_time >= date_from)\
        .order_by('update_time desc')\
        .subquery()

    return db.session.query(sub.c.update_time,
                            func.avg(sub.c.usd_buying),
                            func.avg(sub.c.usd_selling),
                            func.avg(sub.c.eur_buying),
                            func.avg(sub.c.eur_selling)).one()


def get_average_rate_for_date_range(date_from, date_to):
    """Gets average rates for date range."""
    sub = Rate.query\
        .group_by('bank_id')\
        .filter(and_(Rate.update_time >= date_from, Rate.update_time <= date_to))\
        .order_by('update_time desc')\
        .subquery()

    return db.session.query(sub.c.update_time,
                            func.avg(sub.c.usd_buying),
                            func.avg(sub.c.usd_selling),
                            func.avg(sub.c.eur_buying),
                            func.avg(sub.c.eur_selling)).one()


def get_last_update_time():
    """Gets last update time of currency rates."""
    return Rate.query.with_entities(func.max(Rate.update_time)).one()[0]


def get_usd_selling_min_rate():
    """Gets USD selling min rate."""
    return Rate.query.with_entities(func.max(Rate.usd_selling))\
        .filter_by(update_time=get_last_update_time_as_query())\
        .one()[0]


def get_eur_selling_min_rate():
    """Gets EUR selling min rate."""
    return Rate.query.with_entities(func.max(Rate.eur_selling))\
        .filter_by(update_time=get_last_update_time_as_query())\
        .one()[0]


def get_usd_buying_max_rate():
    """Gets USD buying max rate."""
    return Rate.query.with_entities(func.max(Rate.usd_buying))\
        .filter_by(update_time=get_last_update_time_as_query())\
        .one()[0]


def get_eur_buying_max_rate():
    """Gets EUR buying max rate."""
    return Rate.query.with_entities(func.max(Rate.eur_buying))\
        .filter_by(update_time=get_last_update_time_as_query())\
        .one()[0]