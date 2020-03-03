#!/usr/bin/env python3

import os, sys, requests
from time import sleep
from MyLib.GeoLocation import getToken, getAppartmentInfo, processCache

ads = getAppartmentInfo('apartmentInfo')
cache = processCache('addressCache')

key = getToken()
query = 'Denny%20St,%20Ajax,%20ON%20L1Z0C6,%20Canada'
baseURL = "https://us1.locationiq.com/v1/search.php?key=%s" % key 

cacheFile = open('addressCache','a+')
ignoredAds = []
toPrint = "let data = [ \n"
adCounter = 0
for ad in ads:
	adCounter += 1
	if ad.address in cache:
		if  cache[ad.address][0] == "none" or cache[ad.address][1] == "none":
			ignoredAds.append(ad)
			continue
		else:
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
			print("Failed to process output of LocationIQ to a JSON file",file=sys.stderr)
			ignoredAds.append(ad)
			continue
		if "error" in data:
			print("Geocoding API failed to process the following address: " + ad.address,file=sys.stderr)
			ignoredAds.append(ad)
		else:
			if len(data) > 1: print("Geocoding resulted in more than one result, ignoring all except the first one",file=sys.stderr)
			ad.lat = data[0]["lat"]
			ad.lon = data[0]["lon"]
			toPrint += str(ad) + ',\n'
		cacheFile.write('%s --> %s,%s\n' % (ad.address, ad.lat, ad.lon))
		cache[ad.address] = [ad.lat,ad.lon]
		cacheFile.flush()
	if(adCounter % 10 == 0): print("Processed so far: %d/%d" % (adCounter,len(ads)),file=sys.stderr)
toPrint = toPrint[:-2] + "\n]"
print(toPrint)

# print("Ignored Ads:")
# for ad in ignoredAds: print("* " + ad.link)