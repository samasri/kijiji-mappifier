#!/usr/bin/env python3

import urllib.request, time
from bs4 import BeautifulSoup
from MyLib.Scraping import getAdAddress, getPriceOf

failedtrials = 0
def getAds(url, processedLinks, db):
	global failedtrials
	print("  * URL: " + url)
	time.sleep(5)
	fp = urllib.request.urlopen(url)
	mybytes = fp.read()
	soup = BeautifulSoup(mybytes, 'html.parser')

	ignored = 0
	ads = soup.find_all(class_='search-item')
	adCounter = 1
	if len(ads) == 0:
		failedtrials += 1
		if failedtrials > 10:
			print("  * Giving up on page after ten trials...")
			return -1
		print("  * Failed to read page, trying again in one minute")
		time.sleep(60)
		getAds(url, processedLinks,db)
	else: failedtrials = 0
	for ad in ads:
		print("  - Ad %d/%d: " % (adCounter + ignored, len(ads)),end='')

		# Get title and link
		titles = ad.find_all(class_='title')
		if len(titles) != 2:
			ignored += 1
			print ('Error, there are no two tags with class "title" for this ad')
			continue
		title = titles[0].find_all('a')[0].get_text().strip().replace('\n',' ').replace('\r',' ')
		while '  ' in title: title = title.replace('  ',' ')
		link = 'https://www.kijiji.ca' + titles[1]['href']
		
		# Skip already processed entries
		if link in processedLinks:
			adCounter += 1
			print('Hit already saved ad')
			continue
		
		# Get price
		price = getPriceOf(ad)
		if isinstance(price,int) and price < 0:
			if price == -1: print ('Error, more than one price for ad')
			elif price == -2: print ('Price not available, entry ignored')
			elif price == -3: print ('Price not in right format, ignoring this entry')
			else:
				print("  * ERROR: getPriceOf gave an unexpected value")
				print("    * URL: " + url)
				print("    * Returned value: " + price)
			ignored += 1
			continue
		
		# Get address
		address = getAdAddress(link)
		if address == '':
			ignored += 1
			continue
		
		toWrite = title + " --> " + price + " --> " + link + ' --> ' + address + '\n'
		toWrite = toWrite.encode('ascii', 'ignore').decode('ascii') # ignore non-ascii encoded characters
		db.write(toWrite)
		processedLinks.add(link)
		adCounter += 1
		print ('Ad completed')
	db.flush()
	return ignored

# Get already processed ads
processedLinks = set()
try:
	db = open('apartmentInfo')
	for ad in db:
		if not ad: continue
		ad = ad.split(' --> ')
		processedLinks.add(ad[2])
except FileNotFoundError: ... # There is no apartmentInfo collected previouy

# Process new ads
db = open('apartmentInfo','a+')

baseLink = 'https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area'
nbOfPages = 100

for page in range(nbOfPages):
	print("* Checking page: " + str(page + 1) + "/" + str(nbOfPages))
	ignoredAds = getAds(baseLink + '/page-' + str(page) + '/c30349001l1700272?ad=offering', processedLinks, db)
	if ignoredAds >= 0: print(str(ignoredAds) + " ignored ads")
