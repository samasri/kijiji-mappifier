#!/usr/bin/env python3

import os, sys
from time import sleep
from MyLib.GeoLocation import getAppartmentInfo, processCache, getLocation

ads = getAppartmentInfo('apartmentInfo')
cache = processCache('addressCache')

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
		pair = getLocation(ad.address)
		if isinstance(pair, int) and pair < 0:
			if pair == -1:
				print("  Failed to process output of LocationIQ to a JSON file for address: " + ad.address,file=sys.stderr)
				continue
			if pair == -2:
				print("  Geocoding API failed to process the following address: " + ad.address,file=sys.stderr)
				pair = None,None
				# Cache that this is an error
			ignoredAds.append(ad)
		ad.lat,ad.lon = pair[0],pair[1]
		toPrint += str(ad) + ',\n'
		cacheFile.write('%s --> %s,%s\n' % (ad.address, ad.lat, ad.lon))
		cache[ad.address] = [ad.lat,ad.lon]
		cacheFile.flush()
	if(adCounter % 10 == 0): print("Processed so far: %d/%d" % (adCounter,len(ads)),file=sys.stderr)
toPrint = toPrint[:-2] + "\n]"
print(toPrint)

# print("Ignored Ads:")
# for ad in ignoredAds: print("* " + ad.link)