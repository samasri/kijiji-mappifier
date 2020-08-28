import urllib.request, re, time
from bs4 import BeautifulSoup

# Helper function for __getAdAddress
# Uses urllib to open the provided link
# Attempts to retrieve extract the address from it
# Error codes:
# -1: urllib failed to get the address. Most likely the address is wrong
# -2: Connection error, see this bug for more info: https://bugs.python.org/issue26499
# -3: No location found in the html page
# -4: Multiple different locations are found in the html page
def __getAdAddress_direct(link):
	try: fp = urllib.request.urlopen(link)
	except: return -1

	try: mybytes = fp.read()
	except: return -2
    
	soup = BeautifulSoup(mybytes, 'html.parser')
	
	location = soup.findAll(class_=re.compile('address-*'))
	if len(location) < 1: return -3
	elif len(location) > 1: # If multiple locations found, check if they are the same
		first = location[0]
		for l in location:
			if l != first: return -4

	return location[0].get_text().strip()

# Attempts to get the address of a real estate advertisement
# Input:
#   * URL for the advertisement on Kijiji
#   * Number of times we tried reaching this URL and failed before
# Output: Adress of the advertisement
def __getAdAddress(link, failuredConnection, failedProcessing):
	if failuredConnection > 10: return ''
	if failedProcessing > 3: return ''
	address = __getAdAddress_direct(link)

	if isinstance(address,int) and address < 0:
		if address == -1: print("Link is not valid, ignoring: " + link)
		if address == -2:
			if failuredConnection == 0 and failedProcessing == 0: print()
			print("  ~ Connection failure, waiting one minute before trying again")
			time.sleep(60)
			return __getAdAddress(link, failuredConnection + 1, failedProcessing)
		if address == -3:
			if failuredConnection == 0 and failedProcessing == 0: print()
			print("  ~ Cannot find appropriate location, waiting one minute and trying again: ", link)
			time.sleep(60)
			return __getAdAddress(link, failuredConnection, failedProcessing + 1)
		if address == -4: print("More than one different locations are available: ", link)
		return ''

	return address.replace('\n', ' ').replace('\r', '')

# Attempts to get the address of a real estate advertisement
# Input: URL for the advertisement on Kijiji
# Output: Adress of the advertisement
def getAdAddress(link):
    return __getAdAddress(link,0,0)

# Attemps to get the price offered on a real estate advertisement
# Input: A `soup.find_all` result representing a real estate advertisement
# Output: Price
# Error codes:
# -1: More than one price is available
# -2: Price not available (need to contact the landlord privately for price)
# -3: Price is not in the right format
def getPriceOf(ad):
	prices = ad.find_all('div',class_='price')
	if len(prices) != 1: return -1
	else: price = prices[0].get_text().strip()

	if price == 'Please Contact': return -2

	# Remove ads with prices that are not valid numbers
	try: priceFloat = float(price.replace('$','').replace(',',''))
	except: return -3

	return price