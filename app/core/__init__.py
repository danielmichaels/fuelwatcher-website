from flask import Blueprint

"""This creates the core blueprint. """
core = Blueprint('core', __name__)

from . import routes
