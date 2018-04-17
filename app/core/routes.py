import logging
from . import core
from flask import render_template, jsonify, redirect
from app import db, fuelwatch
from fuelwatcher import constants
from app.models import *

logging.basicConfig(level=logging.INFO)


@core.route('/test')
def test():
    fuelwatch.query(suburb='Floreat', product=1)
    xml = fuelwatch.get_xml
    fuelwatch.query(suburb='Floreat', product=2)
    xml1 = fuelwatch.get_xml
    fuelwatch.query(suburb='Floreat', product=4)
    xml2 = fuelwatch.get_xml

    return jsonify(xml, xml1, xml2)


@core.route('/index/<day>')
@core.route('/<day>')
def index(day):
    """User initiated selection of day

    :arg day takes in options {today, yesterday, tomorrow}

    :return index.html with top ten prices for user selected :arg day
    """
    fuelwatch.query(product=1, day=day)
    ulp = fuelwatch.get_xml[:10]
    fuelwatch.query(product=2, day=day)
    p_ulp = fuelwatch.get_xml[:10]
    fuelwatch.query(product=4, day=day)
    dsl = fuelwatch.get_xml[:10]
    fuelwatch.query(product=5, day=day)
    lpg = fuelwatch.get_xml[:10]

    suburbs = constants.SUBURB

    if len(ulp or p_ulp or dsl or lpg) == 0:
        #flash (Check after 1430 AWST)
        return redirect("index/today")

    return render_template('index.html', ulp=ulp, p_ulp=p_ulp, dsl=dsl,
                           lpg=lpg, day=day, suburbs=suburbs)
