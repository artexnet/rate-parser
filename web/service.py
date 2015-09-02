__author__ = 'arthur'

from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

from helpers.service_helper import make_public_bank, make_public_rate, build_average_data_map
from managers import banks_manager, rates_manager


# Shows the corresponding service is running message
@api.route('/status')
def index():
    return "checked: OK"


# Returns all banks list with latest rates
@api.route('/api/v1.0/banks', methods=['GET'])
def get_banks():
    banks = banks_manager.get_banks()
    return jsonify({'banks': map(make_public_bank, banks)})


# Returns selected bank's rates for last month
@api.route('/api/v1.0/banks/<int:bank_id>', methods=['GET'])
def get_bank(bank_id):
    bank = banks_manager.get_bank(bank_id)
    return jsonify({'bank': make_public_bank(bank)})


@api.route('/api/v1.0/banks/<int:bank_id>/rates', methods=['GET'])
def get_bank_rates(bank_id):
    rate = rates_manager.get_bank_latest_rates(bank_id)
    bank = rate.bank
    return jsonify({'bank': make_public_bank(bank), 'rate': make_public_rate(rate)})


@api.route('/api/v1.0/banks/<int:bank_id>/rates/<string:date_from>', methods=['GET'])
def get_bank_rates_from(bank_id, date_from):
    rates = rates_manager.get_bank_rates_from_date(bank_id, date_from)

    if not rates or rates.count == 0:
        return jsonify({'error': 'No data found'})

    bank = rates[0].bank
    return jsonify({'bank': make_public_bank(bank), 'rates': map(make_public_rate, rates)})


@api.route('/api/v1.0/banks/<int:bank_id>/rates/<string:date_from>/<string:date_to>', methods=['GET'])
def get_bank_rates_from_to(bank_id, date_from, date_to):
    rates = rates_manager.get_bank_rates_for_date_range(bank_id, date_from, date_to)

    if not rates or rates.count == 0:
        return jsonify({'error': 'No data found'})

    bank = rates[0].bank
    return jsonify({'bank': make_public_bank(bank), 'rates': map(make_public_rate, rates)})


@api.route('/api/v1.0/rates/average', methods=['GET'])
def get_rates_average():
    rates_average = rates_manager.get_average_rates()
    return jsonify({'average': build_average_data_map(rates_average)})


@api.route('/api/v1.0/rates/average/<string:date_from>', methods=['GET'])
def get_rates_average_from(date_from):
    rates_average = rates_manager.get_average_rates_from_date(date_from)
    return jsonify({'average': build_average_data_map(rates_average)})


@api.route('/api/v1.0/rates/average/<string:date_from>/<string:date_to>', methods=['GET'])
def get_rates_average_from_to(date_from, date_to):
    rates_average = rates_manager.get_average_rate_for_date_range(date_from, date_to)
    return jsonify({'average': build_average_data_map(rates_average)})