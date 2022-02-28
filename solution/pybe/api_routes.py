import logging
from flask import  Response
from flask_restx import Resource, Namespace
from business_logic import import_listings
from database import db
from db_models import Vehicle_Listing as VL_Record, Validation_Errors as VE_Record

logger = logging.getLogger(__name__)

ns = Namespace('listings', description='Vehicle Listings')

@ns.route('/import/<int:provider>/<string:csvname>')
class ImportListingCSV(Resource):

    def get(self,provider,csvname):
        filename = f'{csvname}.csv'
        result = import_listings(provider,filename)
        if result['success']:
            return Response('success', status=200)
        else:
            return Response(result['message'],status=500)

"""@ns.route('/checkmapping')
class TestMapping(Resource):
    def get(self):
        m = generate_field_mappings()
        for i,e in enumerate(m):
            logger.info(f"Mapping file {i} ")
            logger.info(e)
        return Response('success', status=200)"""

@ns.route('/clear')
class ClearListings(Resource):

    def get(self):

        VL_Record.query.delete()
        VE_Record.query.delete()
        db.session.commit()
        return Response('success', status=200)

