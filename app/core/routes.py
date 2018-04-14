import logging
from . import core
from flask import render_template
from app import db
from app.models import *

logging.basicConfig(level=logging.INFO)


@core.route('/')
@core.route('/index')
def index():
    return render_template('index.html')
