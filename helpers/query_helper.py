__author__ = 'arthur'

from models import Rate
from sqlalchemy import func


def get_last_update_time_as_query():
    """Gets rates last update time as sub-query."""
    return Rate.query.with_entities(func.max(Rate.update_time))\
        .subquery()


def get_usd_selling_min_rate_as_query():
    """Gets USD selling min rate as sub-query."""
    return Rate.query.with_entities(func.max(Rate.usd_selling))\
        .filter_by(update_time=get_last_update_time_as_query())\
        .subquery()


def get_eur_selling_min_rate_as_query():
    """Gets EUR selling min rate as sub-query."""
    return Rate.query.with_entities(func.max(Rate.eur_selling))\
        .filter_by(update_time=get_last_update_time_as_query())\
        .subquery()


def get_usd_buying_max_rate_as_query():
    """Gets USD buying max rate as sub-query."""
    return Rate.query.with_entities(func.max(Rate.usd_buying))\
        .filter_by(update_time=get_last_update_time_as_query())\
        .subquery()


def get_eur_buying_max_rate_as_query():
    """Gets EUR buying max rate as sub-query."""
    return Rate.query.with_entities(func.max(Rate.eur_buying))\
        .filter_by(update_time=get_last_update_time_as_query())\
        .subquery()