__author__ = 'arthur'

from flask import Blueprint, jsonify, make_response

err = Blueprint('err', __name__)


@err.errorhandler(400)
def bad_request(error):
    """Returns error message with HTTP 400 code [Bad Request]."""
    return make_response(jsonify(error=str(error), message=error.description), 400)


@err.errorhandler(401)
def unauthorized(error):
    """Returns error message with HTTP 401 code [Unauthorized]."""
    return make_response(jsonify(error=str(error), message=error.description), 401)


@err.errorhandler(404)
def not_found(error):
    """Returns error message with HTTP 404 code [Not Found]."""
    return make_response(jsonify(error=str(error), message=error.description), 404)


@err.errorhandler(500)
def internal_server_error(error):
    """Returns error message with HTTP 500 code [Internal Server Error]."""
    return make_response(jsonify(error=str(error), message=error.description), 500)


@err.errorhandler(501)
def not_implemented(error):
    """Returns error message with HTTP 501 code [Not Implemented]."""
    return make_response(jsonify(error=str(error), message=error.description), 501)