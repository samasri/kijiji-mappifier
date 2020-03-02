import urllib.request
from bs4 import BeautifulSoup
import re

def __getAdAddress(link):
	try:
		fp = urllib.request.urlopen(link)
	except:
		print ("  Link is not valid, ignoring: " + link)
		return ""
	try: mybytes = fp.read()
	except: mybytes = fp.read() # Try again, see this bug for more info: https://bugs.python.org/issue26499
	soup = BeautifulSoup(mybytes, 'html.parser')
	
	location = soup.find_all(class_=re.compile('locationContainer-*'))
	if len(location) != 1:
		print ("  Cannot find appropriate location")
		return ''
	return list(location[0].children)[1].get_text().strip()

# Takes a link for a real estate advertisement and attemps to get the
# price offered
def getAdAddress(link):
	address = __getAdAddress(link)

	if address == '':
		# Trying again helps in some cases
		repeat = 0
		while repeat < 5:
			print("  Trying again...")
			address = __getAdAddress(link)
			if 'address' == '': repeat += 1
			else: repeat = 6
	
	return address


def getPriceOf(ad):
    prices = ad.find_all('div',class_='price')
    if len(prices) != 1: 
        print ('  Error, more than one price for ad: ' + link)
        return -1
    else: price = prices[0].get_text().strip()
    
    # In some cases, landlord would not put the price on Kijiji, instead, asks interested people to contact
    if price == 'Please Contact':
        print ('  Price not found, ignoring entry')
        return -1
    
    # Remove ads with prices that are not valid numbers
    try:
        priceFloat = float(price.replace('$','').replace(',',''))
    except:
        print ('  Price not in right format, ignoring this entry')
        return -1
    return price