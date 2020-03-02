import os, sys, requests
from time import sleep

class Ad:
	def __init__(self, title, price, link, address):
		self.title = title.replace('"','')
		self.price = price
		self.link = link
		self.address = address
		self.lat = "none"
		self.lon = "none"
	
	def __str__(self):
		# assert self.lat != "none" and self.lon != "none"
		jsonStr = '''{
  "title": "%s",
  "price": "%s",
  "link": "%s",
  "address": "%s",
  "lat": "%s",
  "lon": "%s"
}''' % (self.title,self.price,self.link,self.address,self.lat,self.lon)
		return jsonStr

file = open('apartmentInfo')

MAX = 2000
MIN = 0

# Collect data from file
ads = []
for r in file:
	if not r: continue
	r = r.split(' --> ')
	title = r[0].strip()
	price = r[1].strip()[1:].replace(',','')
	link = r[2].strip()
	address = r[3].strip()
	ads.append(Ad(title,price,link,address))
	# Filter by price
	price = int(price[:-3].replace(',',''))
	if price < MIN or price > MAX: continue

key = '859284e3122a88'
query = 'Denny%20St,%20Ajax,%20ON%20L1Z0C6,%20Canada'
baseURL = "https://us1.locationiq.com/v1/search.php?key=%s" % key #&q=%s&format=json" % (key,query)
# r = request
# t("Lon: " + str(data[0]["lon"]))

cache = {}
cacheFile = open('addressCache')
for r in cacheFile:
	r = r.strip()
	if not r: continue
	r = r.split(' --> ')
	cache[r[0]] = r[1].split(',')

cacheFile = open('addressCache','a+')
ignoredAds = []
toPrint = "let data = [ \n"
adCounter = 0
for ad in ads:
	adCounter += 1
	if ad.address in cache:
		# print("Cache hit!",file=sys.stderr)
		ad.lat = cache[ad.address][0]
		ad.lon = cache[ad.address][1]
		toPrint += str(ad) + ',\n'
	else:
		sleep(1)
		query = ad.address
		url = baseURL + "&q=%s&format=json" % (query)
		r = requests.get(url)
		try:
			data = r.json()
		except:
			print("Error processing coordinates via geocoding",file=sys.stderr)
			ignoredAds.append(ad)
			continue
		if "error" in data:
			print("Error retreiving coordinates via geocoding",file=sys.stderr)
			ignoredAds.append(ad)
			continue
		else:
			if len(data) > 1: print("Error: geocoding resulted in more than one result",file=sys.stderr)
			ad.lat = data[0]["lat"]
			ad.lon = data[0]["lon"]
			toPrint += str(ad) + ',\n'
		cacheFile.write('%s --> %s,%s\n' % (ad.address, ad.lat, ad.lon))
		cache[ad.address] = [ad.lat,ad.lon]
		cacheFile.flush()
	# if(adCounter % 10 == 0): print("Processed so far: %d/%d" % (adCounter,len(ads)),file=sys.stderr)
toPrint = toPrint[:-2] + "\n]"
print(toPrint)

print("Ignored Ads:")
for ad in ignoredAds: print("* " + ad.link)