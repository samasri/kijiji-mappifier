import urllib.request
from bs4 import BeautifulSoup

def getAdAddress(link):
	try:
		fp = urllib.request.urlopen(link)
	except:
		print ("Link is not valid, ignoring: " + link)
		return ""
	mybytes = fp.read()
	soup = BeautifulSoup(mybytes, 'html.parser')
	
	location = soup.find_all(class_='locationContainer-118575590')
	if len(location) != 1:
		print ("Cannot find appropriate location: " + str(len(location)))
		return ''
	return list(location[0].children)[1].get_text().strip()

def getAds(url, processedLinks, db):
	fp = urllib.request.urlopen(url)
	mybytes = fp.read()
	soup = BeautifulSoup(mybytes, 'html.parser')

	ignored = 0
	for ad in soup.find_all(class_='search-item'):
		# Get title and link
		titles = ad.find_all(class_='title')
		if len(titles) != 2:
			ignored += 1
			print ('error, there are no two tags with class "title" for this ad')
			continue
		title = titles[0].find_all('a')[0].get_text().strip()
		link = 'https://www.kijiji.ca' + titles[1]['href']
		
		# Skip already processed entries
		if link in processedLinks:
			print('Hit already saved ad!')
			continue
		
		# Get price
		prices = ad.find_all('div',class_='price')
		if len(prices) != 1: 
			ignored += 1
			print ('error, more than one price for ad: ' + link)
			continue
		else: price = prices[0].get_text().strip()
		if price == 'Please Contact':
			print ('price not found, ignoring this entry')
			ignored += 1
			continue
		
		# Get address
		address = getAdAddress(link)
		if address == '':
			ignored += 1
			continue
		
		db.write(title + " --> " + price + " --> " + link + ' --> ' + address + '\n')
		print ('One ad completed!')
	return ignored

# Get already processed ads
db = open('apartmentInfo')
processedLinks = set()
for ad in db:
	if not ad: continue
	ad = ad.split(' --> ')
	processedLinks.add(ad[2])

# Process new ads
db = open('apartmentInfo','a')

baseLink = 'https://www.kijiji.ca/b-house-rental/markham-york-region'
nbOfPages = 40

for page in range(nbOfPages):
	print("Checking page: " + str(page))
	print(getAds(baseLink + '/page-' + str(page) + '/c43l1700272?ad=offering', processedLinks, db))