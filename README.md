# Kijiji Mappifier

I created this tool when I was looking for a place to rent when I came to Toronto. Since Kijiji has no map feature when looking for appartments to rent, this tool scrapes the result pages of Kijiji, finds the price and location of the appartments, and stores them in a CSV database. It then uses [LocationIQ](https://locationiq.com/) API to get the coordinates of each address. Finally, [Leafletjs](https://leafletjs.com/) API is used to display the results on a map.

## Prerequisits

* python 3.5
* BeautifulSoup4
* [LocationIQ](https://locationiq.com/) token
* [Leafletjs](https://leafletjs.com/) token

## How to use

1. Edit the link that is hard coded in [the scraper](https://github.com/samasri/KijijiMapDrawer/blob/master/scraper.py#L88) in order to direct python to the right search pages that should be scraped
2. Edit the [number of pages](https://github.com/samasri/KijijiMapDrawer/blob/master/scraper.py#L89) to tell python how many pages from that search have to be scraped
3. Run the scraper: `python3.5 scraper.py`
4. _apartmentInfo_ is prduced: a csv file that has the results (using `-->` as a delimeter)
5. Set your Leaflet token in [token.js](https://github.com/samasri/KijijiMapDrawer/blob/master/html/token.js)
6. Set your LocationIQ token in [locationiq_token.py](https://github.com/samasri/KijijiMapDrawer/blob/master/MyLib/locationiq_token.py)
7. Create the data for the map: `python3.5 create_map.py > html/data.js`
8. Render _html/result.html_ in a browser to view the results

## Screenshot of the result
