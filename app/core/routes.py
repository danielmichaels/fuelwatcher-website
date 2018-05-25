import logging
from . import core
from flask import render_template, jsonify, redirect, flash, abort, request, \
    url_for
from app import db, fuelwatch
from fuelwatcher import constants
from flask_googlemaps import Map  # remove once /test finished
from .utils import mapping
from app.models import *

logging.basicConfig(level=logging.INFO)


# TODO: JS for day selection '/' grey out 'tomorrow'.
# TODO: tidy up regions.html.
# TODO: create database.
# TODO: highlight selection region on map and bring to top (JS).

@core.route('/test')
def test():
    # fuelwatch.query(suburb='Floreat')
    # resp = fuelwatch.get_xml
    # return render_template('map.html', resp=resp)

    # creating a map in the view
    perth = Map(
        identifier="perth",
        lat=-31.0,
        lng=115.0,
    )
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.4419), (37.5, -122.4)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': 37.4419,
                'lng': -122.1419,
                'infobox': "<b>Hello World</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': 37.4300,
                'lng': -122.1400,
                'infobox': "<b>Hello World from other place</b>"
            }
        ]
    )
    return render_template('map.html', perth=perth, mymap=mymap, sndmap=sndmap)


@core.route('/')
def redirect_index():
    return redirect('index/today')


@core.route('/index/<day>', methods=['POST', 'GET'])
@core.route('/<day>', methods=['POST', 'GET'])
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

    return render_template('index.html', ulp=ulp, p_ulp=p_ulp, dsl=dsl,
                           lpg=lpg, day=day, suburbs=suburbs,
                           product=product)


@core.route('/regions')
def regions():
    regions = constants.REGION

    return render_template('regions.html', regions=regions)


@core.route('/regions/<region>/<product>')
def region(region, product):
    products = constants.PRODUCT
    if product is not None:
        fuelwatch.query(region=int(region), product=int(product))
    else:
        fuelwatch.query(region=int(region), product=product)

    resp = fuelwatch.get_xml
    region_value = constants.REGION.get(int(region))
    product_value = constants.PRODUCT.get(int(product))
    if not resp:
        flash(
            '{product} Not Found in {region}'.format(
                region=region_value, product=product_value))
        return redirect(url_for('core.region', region=region, product=1))
    region_map = mapping(resp)

    return render_template('region.html', region=region, resp=resp,
                           region_value=region_value,
                           region_map=region_map, products=products,
                           product=product, product_value=product_value)


@core.route('/search_results/', methods=['POST', 'GET'])
def search_results():
    product = request.form.get('fuel')
    suburb = request.form.get('suburb')
    product_key = [k for k, v in constants.PRODUCT.items() if v == product][0]
    fuelwatch.query(suburb=suburb, product=product_key)
    resp = fuelwatch.get_xml
    if not resp:
        flash('Sorry! {0} is not availabe in {1} Please try a new search'.
              format(product, suburb))
        return redirect('index/today')
    maps = mapping(resp)
    return render_template('result.html', resp=resp, suburb=suburb,
                           product=product_key, product_value=product,
                           maps=maps)


@core.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@core.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
