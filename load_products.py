import flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

import os
from bs4 import BeautifulSoup
import urllib
import re

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
	print products
	return products

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

global products
products = load_static_products(os.getcwd() + '/static')

