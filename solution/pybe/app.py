import logging.config
import logging
import os
from flask import Flask
from restplus import api
from restplus import blueprint as bp
from api_routes import ns as listings_namespace
from database import db



logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s][%(levelname)s][%(thread)d][%(module)s] - %(message)s',
    handlers=[
        #logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
log = logging.getLogger(__name__)

# configure ORM connection
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://sa:Password123@postgres:5432/postgres'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# set up database
db.init_app(app)
with app.app_context():
    db.reflect()

api.init_app(bp)
api.add_namespace(listings_namespace)
app.register_blueprint(bp)
log.info("API has started")

if __name__ == '__main__':
    log.info('*** Starting built in flask server')
    run_params = {
        'host': '0.0.0.0',
        'port': '8008',
        'debug': True
    }
    log.info(f"Using run_params: {run_params}")
    app.run(**run_params)
