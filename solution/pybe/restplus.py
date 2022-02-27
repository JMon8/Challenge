import logging
from flask import Blueprint, jsonify
from flask_restx import Api

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Vehicle Listings Importer',
            description=' Endpoints for Vehicle Listings Importer\n\n[swagger.json](/api/swagger.json)',)

blueprint = Blueprint('api', __name__, url_prefix='/api')

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occured.'
    log.exception(message)
    return {'message':message}, 500
