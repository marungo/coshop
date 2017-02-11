from bs4 import BeautifulSoup
import urllib

r = urllib.urlopen('https://www.amazon.com/ORVILLE-REDENBA-\
					Natural-Microwave-Popcorn/dp/B008V9997C/\
					ref=sr_1_1_a_it?ie=UTF8&qid=1486851122&sr=\
					8-1&keywords=popcorn+orvills').read()


soup = BeautifulSoup(r, 'html.parser')

# data = soup.prettify()
data = soup.find_all('div', class_='imgTagWrapper')

for tag in data:
	# print tag.name, '\n'
	for t in tag:
		# print t.name
		if t.name == 'img':
			# print t.attrs
			print t['src']
# print '\n'.join(data)
# print type(data)
# print data
