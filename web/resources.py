__author__ = 'arthur'

from flask import Blueprint, jsonify

rs = Blueprint('rs', __name__)


@rs.route('/resources')
def resources():
    data = {
        'index': '/status',
        'get_banks': '/api/v1.0/banks',
        'get_bank': '/api/v1.0/banks/{bank_id}',
        'get_bank_rates': '/api/v1.0/banks/{bank_id}/rates',
        'get_bank_rates_from': '/api/v1.0/banks/{bank_id}/rates/{yyyy-MM-dd}',
        'get_bank_rates_from_to': '/api/v1.0/banks/{bank_id}/rates/{yyyy-MM-dd}/{yyyy-MM-dd}',
        'get_rates_average': '/api/v1.0/rates/average',
        'get_rates_average_from': '/api/v1.0/rates/average/{yyyy-MM-dd}',
        'get_rates_average_from_to': '/api/v1.0/rates/average/{yyyy-MM-dd}/{yyyy-MM-dd}',
    }
    return jsonify(resources=data)



