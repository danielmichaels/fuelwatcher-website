# Imports
from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from fuelwatcher import FuelWatch
from flask_googlemaps import GoogleMaps
# Instantiations

db = SQLAlchemy()
fuelwatch = FuelWatch()
google_maps = GoogleMaps(key='AIzaSyDeKO22YmX_a5lsoeImXUkWx7d0H36k3sY')



def create_app(config_name):
    """Flask Application Factory."""
    # ------- Flask Setup
    app = Flask(__name__)
    # app.config.from_object(config['default'])
    app.config.from_object(config[config_name])

    # ------ Application Factory

    db.init_app(app)
    # google_maps.init_app(app)
    GoogleMaps(app)
    # with app.test_request_context():
    with app.app_context():
        """Creates context to drive the db.create_all()"""
        db.create_all()

    from .core import core as core
    app.register_blueprint(core)
    '''
    Blueprint was required after making the application factory.
    As the app instance is created and configured at runtime and thus the 'app'
    has already created, you cannot access the 'app' after this. 
    I.e. the app in app.route is inaccessible: blueprints mitigate this.
    '''

    return app
