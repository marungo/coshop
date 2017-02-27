#!/usr/bin/env python
import flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import re

import os
import load_products


# Create the application.
APP = flask.Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zkuzqmqystamvh:972956f846e943664bf64b437c0628f9518dda2d1616abd7f053a3bcfe373bf8@ec2-184-72-249-88.compute-1.amazonaws.com:5432/da1iad07bev1ji'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
global db
db = SQLAlchemy(APP)

import models
from models import User
from models import Product


@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    #build_product('https://www.amazon.com/dp/B01D2ZN5LK/ref=twister_B01HTRXLB6?_encoding=UTF8&psc=1')
    return flask.render_template('index.html')


@APP.route('/form', methods=['GET', 'POST'])
def my_form_post():
	print 'hello'

	url = flask.request.form['amazonProduct']
	# get Asin from url
	r = re.compile("(?<=/dp/).*(?=/)")
	global product_asin
	product_asin = r.findall(url)[0]
		
	products = load_products.products

	try:
		product_info = products[product_asin]
	except KeyError:
		product_info = products.values()[0]

	#check if product is already in database
	prods = Product.query.all()
	if len(prods) > 0:
		print prods
	else:
		print "PRODUCT DID NOT EXIST BEFORE"
		# new_prod = Product()

	product_info['url'] = url

	return flask.render_template('form.html', product_info=product_info)

# @APP.route('/done', methods=['GET', 'POST'])
# def submit_form():
# 	return flask.render_template('done.html')

if __name__ == "__main__":
    APP.debug=False
    APP.run()
