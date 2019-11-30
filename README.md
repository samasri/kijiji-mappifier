# Kijiji Mappifier

I created this tool when I was looking for a place to rent when I came to Toronto. Since Kijiji has no map feature when looking for appartments to rent, this tool scrapes the result pages of Kijiji, finds the price and location of the appartments, and stores them in a database. With the help of [gmplot](https://github.com/vgm64/gmplot) (an python library that gives access to some of the Google Map JavaScript API), I could visualize the results on a map.

Since I had to edit the gmplot source code a bit for my use, I got the source code and added it to my repo directly (also saves on dependency).

## Prerequisits

* python 3.5
* BeautifulSoup4
* Google Map API key (will cost some money, but it's pay as you go, so it should cost few cents to few dollars depending on how many Kijiji ads you plan to process)

## How to use

1. Edit the link that is hard coded in [the scraper](https://github.com/samasri/KijijiMapDrawer/blob/master/scraper.py#L88) in order to direct python to the right search pages that should be scraped
2. Edit the [number of pages](https://github.com/samasri/KijijiMapDrawer/blob/master/scraper.py#L89) to tell python how many pages from that search have to be scraped
3. Run `python3.5 scraper.py`
4. You will get _apartmentInfo_, a csv file that has the results (delimeter = `-->`)
5. Set your Google Map API key in [create_map](https://github.com/samasri/KijijiMapDrawer/blob/master/create_map.py#L28) (the API key should have _Geocoding API_ and _Maps JavaScript API_ enabled)
6. Run `python3.5 create_map.py` to create the html page

## Screenshot of the result

![Screenshot](https://github.com/samasri/KijijiMapDrawer/blob/master/Screenshot.png)

## Known issues

* _create_map_ crashes at some of the scraped entries. This happens when the geocode api cannot find the address given. This error should be handled in python.
