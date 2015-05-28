__author__ = 'arthur'

from flask import Blueprint, jsonify, make_response

err = Blueprint('err', __name__)


# Returns error message with HTTP 400 code [Bad Request]
@err.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'Bad Request': error.description}), 400)


# Returns error message with HTTP 401 code [Unauthorized]
@err.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'Unauthorized': error.description}), 401)


# Returns error message with HTTP 404 code [Not Found]
@err.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Not Found': error.description}), 404)


# Returns error message with HTTP 500 code [Internal Server Error]
@err.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'Internal Server Error': error.description}), 500)


# Returns error message with HTTP 500 code [Not Implemented]
@err.errorhandler(501)
def not_implemented(error):
    return make_response(jsonify({'Not Implemented': error.description}), 501)