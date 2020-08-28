from MyLib.locationiq_token import token
import sys, requests
baseURL = "https://us1.locationiq.com/v1/search.php?key=%s" % token # For API calls

debug = True

class Ad:
	def __init__(self, title, price, link, address):
		self.title = title.replace('"','')
		self.price = float(price)
		self.link = link
		self.address = address
		self.lat = "none"
		self.lon = "none"
	
	def __str__(self):
		# assert self.lat != "none" and self.lon != "none"
		jsonStr = '''{
  "title": "%s",
  "price": %f,
  "link": "%s",
  "address": "%s",
  "lat": "%s",
  "lon": "%s"
}''' % (self.title,self.price,self.link,self.address,self.lat,self.lon)
		return jsonStr

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def getAppartmentInfo(filePath):
    inputFile = open(filePath)

    # Collect data from file
    ads = []
    for r in inputFile:
        if not r: continue
        r = r.split(' --> ')
        if len(r) != 4:
            eprint("---------- ERROR in: %s" % r)
            continue
        title = r[0].strip()
        price = r[1].strip()[1:].replace(',','')
        link = r[2].strip()
        address = r[3].strip()
        ads.append(Ad(title,price,link,address))
        # Filter by price
        price = int(price[:-3].replace(',',''))
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

def getLocation(query):
    url = baseURL + "&q=%s&format=json" % (query)
    r = requests.get(url)
    try: data = r.json()
    except: return -1
    if "error" in data: return -2
    if len(data) > 1:
        if debug:
            print("  Geocoding resulted in more than one result, ignoring all except the first one",file=sys.stderr)
            for d in data:
                print(" - %s" % d["display_name"],file=sys.stderr)
    return data[0]["lat"],data[0]["lon"]

def getToken():
    return token