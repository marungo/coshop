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


# Create the application.
APP = flask.Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zkuzqmqystamvh:972956f846e943664bf64b437c0628f9518dda2d1616abd7f053a3bcfe373bf8@ec2-184-72-249-88.compute-1.amazonaws.com:5432/da1iad07bev1ji'
db = SQLAlchemy(APP)


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

#APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/maryruthngo'
#db = SQLAlchemy(APP)
# APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/maryruthngo'
# db = SQLAlchemy(APP)

def add_product_to_db(product):
	prod = Product(asin=product['asin'], title=product['title'],
					price=product['price'][0], unit_price=product['unit_price'],
					pack_of=product['pack_of'])
	db.session.add(prod)
	db.session.commit()


def load_static_products(path):
	""" Returns a dictionary of form {asin: {productinfo dict}} for a set of
	static product html files in a given directory
	"""
	products = {}

	for f in os.listdir(path):
		if f.endswith('.htm') or f.endswith('html'):

			with open(path + '/' + f, 'rU') as f_open:
				print path + '/' + f
				soup = BeautifulSoup(f_open, 'html.parser')

			with open(path + '/' + f, 'rU') as f_open:
				text = '\n'.join(f_open.readlines())
				# print type(text)
				# print len(text)

			# get Asin ID
			r = re.compile("(?<=\"currentAsin\" : \").*(?=\")")
			asin = r.findall(text)[0]
			print asin

			# get product info
			products[asin] = build_product(soup)
			products[asin]['asin'] = asin
			products[asin]['portions_available'] = 0
			products[asin]['num_collaborators'] = 0
	return products


# def fake_build_product():
# 	product = {'image': 'pics/laundry.jpg',
# 			   'title': 'Tide Original Scent HE Turbo Clean Liquid Laundry Detergent, 50 Fl Oz (32 Loads), 2 Count',
# 			   'price': 10.77,
# 			   'pack_of': 2}
# 	return product

def build_product(soup):
	product = {}
	# r = urllib.urlopen(url).read()
	# # print r
	# soup = BeautifulSoup(r, 'html.parser')
	# print soup
	####################### Image Scraping #####################
	img_data = soup.find_all('div', class_='imgTagWrapper')
	# print "img: ", img_data
	for tag in img_data:
		for t in tag:
			if t.name == 'img':
				# print t['src']
				product['image'] = t['src']

	####################### Title Scraping #####################
	title_data = soup.find_all('span', id='productTitle')
	if len(title_data) > 1:
		print 'TITLE DATA IS LENGTH: ', len(title_data)

	# print title_data
	for tag in title_data:
		title = tag.contents[0].strip()
		product['title'] = title
		# print title

	pack_of = title.split('Pack of')
	if len(pack_of) == 1:
		#no packs - just product with 1 unit
		pack_of = 1
	else:
		# clean result
		pack_of = pack_of[1].split(")")[0].strip().split(' ')[0]

	#hard-code one small bug away:
	if pack_of == 'three':
		pack_of = '3'

	product['pack_of'] = str(pack_of)

	####################### Price Scraping #####################
	price_data = soup.find_all('div', id='price_feature_div')[0]

	# CASE 1: product with sale
	snsPrice = price_data.find_all('div', id='snsPrice')
	price = []
	if len(snsPrice) > 0:
		for s in snsPrice:
			spans = s.find_all('span', class_=re.compile('price'))
			for sp in spans:
				price.append(sp.contents[0].strip())
			# print 'PRIME PRODUCT with sale: ', ' '.join(price)
	else:
		# CASE 2: produce with no sale
		primePrice = soup.find_all('div', id='price_feature_div')
		for s in primePrice:
			trs = s.find_all('span', id=re.compile('ourprice'))
			for s in trs:
				price.append(s.contents[0].strip())
			# print 'PRIME PRODUCT no sale: ', ' '.join(price)


	product['price'] = price
	product['unit_price'] = '${:,.2f}'.format(float(price[0].split('$')[1])/float(pack_of))
	####################### END Price Scraping ####################
	return product

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    #build_product('https://www.amazon.com/dp/B01D2ZN5LK/ref=twister_B01HTRXLB6?_encoding=UTF8&psc=1')
    return flask.render_template('index.html')

@APP.before_request
def get_products():
	global products
	products = load_static_products(os.getcwd() + '/static')

@APP.route('/form', methods=['GET', 'POST'])
def my_form_post():
	print 'hello'
	url = flask.request.form['amazonProduct']
	# get Asin from url
	r = re.compile("(?<=/dp/).*(?=/)")
	product_asin = r.findall(url)[0]

    # product_info = fake_build_product()
	try:
		product_info = products[product_asin]
	except KeyError:
		product_info = products.values()[0]

	#check if product is already in database
	# prod = Product.query.all()
	# if prod is None:
		# new_prod = Product()


	return flask.render_template('form.html', product_info=product_info)

@APP.route('/done', methods=['GET', 'POST'])
def submit_form():
	return flask.render_template('done.html')


# @APP.route('/submit_form', methods=['GET', 'POST'])
# def post_product():
#

if __name__ == "__main__":
    APP.debug=False
    APP.run()
