#!/usr/bin/env python

import flask
from flask import request
#from flask_sqlalchemy import SQLAlchemy

import os
from bs4 import BeautifulSoup
import urllib
import re


# Create the application.
APP = flask.Flask(__name__)

#APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/maryruthngo'
#db = SQLAlchemy(APP)
# APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/maryruthngo'
# db = SQLAlchemy(APP)

def load_static_sites(path):
	for f in os.listdir(os.getcwd() + '/' + path):
		if f.endswith('.htm') or f.endswith('html'):
			soup = BeautifulSoup(f, 'html.parser')
			build_product(soup)

def build_product(soup):
	# product = {}
	# r = urllib.urlopen(url).read()
	# # print r
	# soup = BeautifulSoup(r, 'html.parser')
	# print soup
	####################### Image Scraping #####################
	img_data = soup.find_all('div', class_='imgTagWrapper')
	print "img: ", img_data
	for tag in img_data:
		for t in tag:
			if t.name == 'img':
				# print t['src']
				product['image'] = t['src']

	####################### Title Scraping #####################
	title_data = soup.find_all('span', id='productTitle')
	if len(title_data) > 1:
		print 'TITLE DATA IS LENGTH: ', len(title_data)

	print title_data
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
	####################### END Price Scraping #####################
	return product

# ????? why is this here
# @APP.route('/')
# def index():
#     """ Displays the index page accessible at '/'
#     """
#     build_product('https://www.amazon.com/dp/B01D2ZN5LK/ref=twister_B01HTRXLB6?_encoding=UTF8&psc=1')
#     return flask.render_template('index.html')

@APP.route('/', methods=['POST'])
def my_form_post():
    print "inside!"
    url = flask.request.form['amazonProduct']
    print url
    product_info = build_product(url)
    print product_info
    return flask.render_template('productInfo.html', product_info=product_info)

if __name__ == '__main__':
    APP.debug=False
    APP.run()
