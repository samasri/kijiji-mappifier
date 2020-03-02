import urllib.request
from bs4 import BeautifulSoup
from MyLib.Scraping import getAdAddress, getPriceOf

def getAds(url, processedLinks, db):
	fp = urllib.request.urlopen(url)
	mybytes = fp.read()
	soup = BeautifulSoup(mybytes, 'html.parser')

	ignored = 0
	ads = soup.find_all(class_='search-item')
	adCounter = 0
	for ad in ads:
		# Get title and link
		titles = ad.find_all(class_='title')
		if len(titles) != 2:
			ignored += 1
			print ('  Error, there are no two tags with class "title" for this ad')
			continue
		title = titles[0].find_all('a')[0].get_text().strip()
		link = 'https://www.kijiji.ca' + titles[1]['href']
		
		# Skip already processed entries
		if link in processedLinks:
			adCounter += 1
			print('  Hit already saved ad: %d/%d'% (adCounter, len(ads)))
			continue
		
		# Get price
		price = getPriceOf(ad)
		if price == -1:
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
		print ('  Ad completed: %d/%d' % (adCounter, len(ads)))
	db.flush()
	return ignored

# Get already processed ads
db = open('apartmentInfo')
processedLinks = set()
for ad in db:
	if not ad: continue
	ad = ad.split(' --> ')
	processedLinks.add(ad[2])

# Process new ads
db = open('apartmentInfo','a+')

baseLink = 'https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area'
nbOfPages = 40

for page in range(nbOfPages):
	print("Checking page: " + str(page + 1) + "/" + str(nbOfPages))
	ignoredAds = getAds(baseLink + '/page-' + str(page) + '/c30349001l1700272?ad=offering', processedLinks, db)
	print(str(ignoredAds) + " ignored ads")