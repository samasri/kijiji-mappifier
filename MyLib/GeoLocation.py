from MyLib.locationiq_token import token

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

def getAppartmentInfo(filePath):
    inputFile = open(filePath)

    MAX = 2000
    MIN = 0

    # Collect data from file
    ads = []
    for r in inputFile:
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
    return ads

def processCache(filePath):
    cache = {}
    cacheFile = open(filePath)
    for r in cacheFile:
        r = r.strip()
        if not r: continue
        r = r.split(' --> ')
        cache[r[0]] = r[1].split(',')
    return cache

def getToken():
    return token