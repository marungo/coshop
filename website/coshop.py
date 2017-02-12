#!/usr/bin/env python

import flask
import os

from bs4 import BeautifulSoup
import urllib
import re


# Create the application.
APP = flask.Flask(__name__)

def build_product(url):
	product = {}
	r = urllib.urlopen(url).read()
	soup = BeautifulSoup(r, 'html.parser')

	####################### Image Scraping #####################
	img_data = soup.find_all('div', class_='imgTagWrapper')

	for tag in img_data:
		for t in tag:
			if t.name == 'img':
				# print t['src']
				product['image'] = t['src']

	####################### Title Scraping #####################
	title_data = soup.find_all('span', id='productTitle')	
	if len(title_data) > 1:
		print 'TITLE DATA IS LENGTH: ', len(title_data)

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

@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('index.html')

@APP.route('/add', methods=['POST'])
def my_form_post():
    url = request.form['text']
    product = build_product(url)
    print product


if __name__ == '__main__':
    APP.debug=True
    APP.run()
