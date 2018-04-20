import logging
from . import core
from flask import render_template, jsonify, redirect, flash, abort
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


@core.route('/search_results/<product>/<suburb>')
def search_results(product, suburb):
    fuelwatch.query(suburb=suburb, product=int(product))
    resp = fuelwatch.get_xml
    product_value = constants.PRODUCT.get(int(product))
    if not resp:
        flash('Sorry! {0} is not availabe in {1} Please try a new search'.
              format(product_value, suburb))
        return redirect('index/today')
    return render_template('result.html', resp=resp, suburb=suburb)

@core.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@core.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
