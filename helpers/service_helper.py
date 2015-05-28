__author__ = 'arthur'

from datetime import datetime
from flask import url_for


# Helpers
def make_public_bank(bank):
    uri = url_for('.get_bank', bank_id=bank.id, _external=True)
    return {
        'uri': uri,
        'uri_logo': bank.uri_logo,
        'name_am': bank.name_am,
        'name_en': bank.name_en,
        'name_ru': bank.name_ru,
        'update_time': bank.update_time,
    }


def make_public_rate(rate):
    uri = url_for('.get_bank_rates', bank_id=rate.bank_id, _external=True)
    return {
        'uri': uri,
        'update_time': rate.update_time,
        'declared_update_time': rate.declared_update_time,
        'usd_buying': rate.usd_buying,
        'usd_selling': rate.usd_selling,
        'eur_buying': rate.eur_buying,
        'eur_selling': rate.eur_selling,
    }

def build_average_data_map(average):
    return {
        'current time': datetime.now(),
        'rate updates since': average[0],
        'usd buying': average[1],
        'usd selling': average[2],
        'eur buying': average[3],
        'eur selling': average[4],
    }
