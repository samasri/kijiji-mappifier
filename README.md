# Kijiji Mappifier
I created this tool when I was looking for a place to rent when I came to Toronto. Since Kijiji has no map feature when looking for appartments to rent, this tool scrapes the result pages of Kijiji, finds the price and location of the appartments, and stores them in a database. With the help of [Mapping Sheets](https://www.thexs.ca/xsmapping) (an add-on for Google Spreadsheets), the results are visualized on a map.

I used this app via Bash on Ubuntu 18 on Windows 10

# Prerequisits
* python 3.5
* BeautifulSoup4
* Google Drive account
* [Mapping Sheets](https://www.thexs.ca/xsmapping) add-on installed on the Google Drive account

# How to use
1. Edit the link that is hard coded in [the scraper](https://github.com/samasri/KijijiMapDrawer/blob/master/scraper.py#L77) in order to direct python to the right search pages that should be scraped
2. Edit the [number of pages](https://github.com/samasri/KijijiMapDrawer/blob/master/scraper.py#L73) to tell python how many pages from that search have to be scraped
3. Run `python3.5 scraper.py`
4. You will get _apartmentInfo_, a csv file that has the results (delimeter = `-->`)
5. Run `python3.5 processingAppartmentInfo.py` in order to convert that to a csv file readable by Google Spreadsheets (delimeter = `=`). In addition, this file parses the price and filters the appartments by price. The price that is used for filtering is in the _processingAppartmentInfo_ script [here](https://github.com/samasri/KijijiMapDrawer/blob/master/processingAppartmentInfo.py#L12)