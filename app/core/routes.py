import logging
from . import core
from flask import render_template, jsonify, redirect, flash
from app import db, fuelwatch
from fuelwatcher import constants
from app.models import *

logging.basicConfig(level=logging.INFO)


@core.route('/test')
def test():
    suburbs, product = constants.SUBURB, constants.PRODUCT
    fuelwatch.query(product=1)
    resp = fuelwatch.get_xml[:10]
    return jsonify(resp)
    # return render_template('index.html', product=product.values(),
    #                        suburbs=suburbs)


@core.route('/')
def redirect_index():
    return redirect('index/today')


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

    suburbs, product = constants.SUBURB, constants.PRODUCT
    surrounding = ['yes', 'no']

    # if len(ulp or p_ulp or dsl or lpg) == 0:
    # if not (ulp or p_ulp or dsl or lpg):
    # flash (Check after 1430 AWST)
    # return redirect("index/today")

    return render_template('index.html', ulp=ulp, p_ulp=p_ulp, dsl=dsl,
                           lpg=lpg, day=day, suburbs=suburbs,
                           product=product.values(), surrounding=surrounding)


@core.route('/regions')
def regions():
    regions = constants.REGION

    return render_template('regions.html', regions=regions)


@core.route('/regions/<region>')
def region(region):

    resp = None
    if fuelwatch.query(region=int(region)):
        resp = fuelwatch.get_xml
        region_value = constants.REGION.get(int(region))
        return render_template('region.html', region=region_value, resp=resp)
    if not fuelwatch.query(region=int(region)):
        # flash('Error Searching {region} Please Try Again Later'.format(
        # region=region))
        return redirect('index/today')

    return render_template('region.html', region=region, resp=resp)


@core.route('/search_results/<product>/<suburb>')
def search_results(product, suburb):
    mock = {'price': 3, 'title': product, 'trading-name': 'trade name',
            'address': suburb}

    # for products in constants.PRODUCT:
    #     product = products
    for k,v in constants.PRODUCT:
        if k == product:
            product = v

    # for k,v in constants.PRODUCT:
    #     v = product

    if not fuelwatch.query(suburb=suburb, product=product):
        return jsonify(mock)
    else:
        resp = fuelwatch.get_xml

    # if fuelwatch.query(suburb=suburb, product=product):
    #     resp = fuelwatch.get_xml

    return render_template('result.html', suburb=suburb, product=product,
                           resp=resp)
