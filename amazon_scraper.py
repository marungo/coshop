from bs4 import BeautifulSoup
import urllib
import re
import os

#example
# products = ['https://www.amazon.com/Highlands-Argyle-Mens-Golf-Collection/dp/B00EDQW9G0/ref=sr_1_50?ie=UTF8&qid=1486852744&sr=8-50-spons&keywords=socks&psc=1',
# 			'https://www.amazon.com/Annies-Macaroni-Cheese-Microwave-Cheddar/dp/B00D7D1Y7U/ref=sr_1_1?ie=UTF8&qid=1486850821&sr=8-1-spons&keywords=annie%27s+mac+and+cheese&psc=1',
# 			'https://www.amazon.com/dp/B00RNEBB90/ref=twister_B00RNEBB6S?_encoding=UTF8&th=1',
# 			'https://www.amazon.com/dp/B01D2ZN5LK/ref=twister_B01HTRXLB6?_encoding=UTF8&psc=1']

def load_static_sites(path):
	for f in os.listdir(os.getcwd() + '/' + path):
		if f.endswith('.htm') or f.endswith('html'):
			soup = BeautifulSoup(f, 'html.parser')
			build_product(soup)



def load_site_url(url):
	r = urllib.urlopen(url).read()
	soup = BeautifulSoup(r, 'html.parser')
	return soup

def build_product(soup):
	product = {}

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


if __name__ == '__main__':
	for url in products:
		print build_product(url)
