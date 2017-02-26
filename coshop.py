#!/usr/bin/env python

import flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

import os
from bs4 import BeautifulSoup
import urllib
import re


# Create the application.
APP = flask.Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql-flat-48765'
db = SQLAlchemy(APP)

#APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/maryruthngo'
#db = SQLAlchemy(APP)
# APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/maryruthngo'
# db = SQLAlchemy(APP)

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
	# print pack_of
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
	product['unit_price'] = int(price[0].split('$')[1]) / float(pack_of)
	####################### END Price Scraping #####################
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
	return flask.render_template('form.html', product_info=product_info)

# @APP.route('/submit_form', methods=['GET', 'POST'])
# def post_product():
#

if __name__ == "__main__":
    APP.debug=False
    APP.run()
