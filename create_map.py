import gmplot 
import os

class Ad:
	def __init__(self, title, price, link, address):
		self.title = title
		self.price = price
		self.link = link
		self.address = address

file = open('apartmentInfo')

max = 2000
min = 0
ads = []
for r in file:
	if not r: continue
	r = r.split(' --> ')
	title = r[0].strip()
	price = r[1].strip()[1:].replace(',','')
	link = r[2].strip()
	address = r[3].strip()
	ads.append(Ad(title,price,link,address))

	price = int(price[:-3].replace(',',''))
	if price < min or price > max: continue

gmap = gmplot.GoogleMapPlotter(43.756191, -79.353349, 12, 'GOOGLE_API') # Initialize map in Ontario
for ad in ads:
	lat, lng = gmap.geocode(ad.address)
	gmap.marker(lat,lng, 'cornflowerblue', title=ad.price, website=ad.link)

# Pass the absolute path 
gmap.draw(os.path.join(os.path.dirname(__file__), 'results.html')) 