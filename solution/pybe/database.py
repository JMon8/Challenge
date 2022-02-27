import logging
from flask_sqlalchemy import SQLAlchemy

logging.getLogger('sqlalchemy').setLevel(logging.INFO)

db = SQLAlchemy()