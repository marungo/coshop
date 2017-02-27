#!/usr/bin/env python

import flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

import os
from bs4 import BeautifulSoup
import urllib
import re

#coshop db
# import coshopdb
import load_products


# Create the application.
APP = flask.Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zkuzqmqystamvh:972956f846e943664bf64b437c0628f9518dda2d1616abd7f053a3bcfe373bf8@ec2-184-72-249-88.compute-1.amazonaws.com:5432/da1iad07bev1ji'
db = SQLAlchemy(APP)

############ DATABASE ###############
commits = db.Table('commits',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('prod_id', db.Integer, db.ForeignKey('product.asin'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    # products = db.relationship('Product', secondary=commits, 
    # 				backref=db.backref('user',lazy='select'), lazy='select')

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name


class Product(db.Model):
    asin = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    price = db.Column(db.String(10))
    unit_price = db.Column(db.String(10))
    pack_of = db.Column(db.String(10))
    # users = db.relationship('User', backref=db.backref('product',
    # 							lazy='dynamic'))


    def __init__(self, title, price, pack_of):
        self.title = title
        self.price = price
        self.pack_of = pack_of

    def __repr__(self):
        return '<Title %r>' % self.title

def add_product_to_db(product):
	prod = Product(asin=product['asin'], title=product['title'],
					price=product['price'][0], unit_price=product['unit_price'],
					pack_of=product['pack_of'])
	db.session.add(prod)
	db.session.commit()

############ END DATABASE ###############


@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    #build_product('https://www.amazon.com/dp/B01D2ZN5LK/ref=twister_B01HTRXLB6?_encoding=UTF8&psc=1')
    return flask.render_template('index.html')

# @APP.before_request
# def get_products():
	# products = load_static_products(os.getcwd() + '/static')

# @APP.route('/getasin', methods=['GET', 'POST'])
# def index():
#     """ Displays the index page accessible at '/'
#     """
#     #build_product('https://www.amazon.com/dp/B01D2ZN5LK/ref=twister_B01HTRXLB6?_encoding=UTF8&psc=1')
#     url = flask.request.form['amazonProduct']
# 	# get Asin from url
# 	r = re.compile("(?<=/dp/).*(?=/)")
# 	global product_asin
# 	product_asin = r.findall(url)[0]
#     return my_form_post(product_asin)


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
	# prod = Product.query.all()
	# if prod is None:
		# new_prod = Product()

	product_info['url'] = url

	return flask.render_template('form.html', product_info=product_info)

# @APP.route('/done', methods=['GET', 'POST'])
# def submit_form():
# 	return flask.render_template('done.html')

if __name__ == "__main__":
    APP.debug=False
    APP.run()
