import logging
from . import core
from flask import render_template, jsonify
from app import db, fuelwatch
from app.models import *

logging.basicConfig(level=logging.INFO)


@core.route('/')
@core.route('/index')
def index():
    return render_template('index.html')

@core.route('/test')
def test():
    fuelwatch.query(suburb='Floreat', product=1)
    xml = fuelwatch.get_xml
    fuelwatch.query(suburb='Floreat', product=2)
    xml1 = fuelwatch.get_xml
    fuelwatch.query(suburb='Floreat', product=4)
    xml2 = fuelwatch.get_xml

    return jsonify(xml, xml1, xml2)

@core.route('/example')
def example():
    fuelwatch.query(product=1)
    ulp = fuelwatch.get_xml[:10]
    fuelwatch.query(product=2)
    p_ulp = fuelwatch.get_xml[:10]
    fuelwatch.query(product=4)
    dsl = fuelwatch.get_xml[:10]
    fuelwatch.query(product=5)
    lpg = fuelwatch.get_xml[:10]
    return render_template('index.html', ulp=ulp, p_ulp=p_ulp, dsl=dsl, lpg=lpg)
