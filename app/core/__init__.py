from flask import Blueprint

'''
This creates the blueprint for blog
'''
core = Blueprint('core', __name__)

from . import routes
