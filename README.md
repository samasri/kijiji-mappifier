# Kijiji Mappifier

I created this tool after I moved to Toronto and was looking for a place to rent. Since Kijiji has no map feature when looking for appartments to rent, this tool scrapes the result pages of Kijiji, finds the price and location of the appartments, and stores them in a CSV database. It then uses [LocationIQ](https://locationiq.com/) API to get the coordinates of each address. Finally, [Leafletjs](https://leafletjs.com/) API is used to display the results on a map.

## Prerequisits

* python 3.5
* BeautifulSoup4
* [LocationIQ](https://locationiq.com/) token
* [Leafletjs](https://leafletjs.com/) token

## How to use

1. Edit the link that is hard coded in [the scraper](https://github.com/samasri/KijijiMapDrawer/blob/master/scraper.py#L88) in order to direct python to the right search pages that should be scraped
2. Edit the [number of pages](https://github.com/samasri/KijijiMapDrawer/blob/master/scraper.py#L89) to tell python how many pages from that search have to be scraped
3. Set your LocationIQ token in [locationiq_token.py](https://github.com/samasri/KijijiMapDrawer/blob/master/MyLib/locationiq_token.py)
4. Run the scraper: `python3.5 scraper.py`. A csv result file (_apartmentInfo_) is produced (using `-->` as a delimeter).
5. Set your Leaflet token in [token.js](https://github.com/samasri/KijijiMapDrawer/blob/master/html/token.js)
6. Create the data for the map: `python3.5 create_data.py > html/data.js`
7. Render _html/result.html_ in a browser to view the results

## Screenshots of the result

* ![screenshot1](https://user-images.githubusercontent.com/12204690/75831760-63387f00-5d82-11ea-8693-81547269e25d.png)

* ![screenshot2](https://user-images.githubusercontent.com/12204690/75831751-5b78da80-5d82-11ea-9a25-e89695df0ac9.png)

* ![screenshot3](https://user-images.githubusercontent.com/12204690/75831768-6df31400-5d82-11ea-80a1-dd8f3139cfc6.png)

* ![screenshot4](https://user-images.githubusercontent.com/12204690/75831783-7c413000-5d82-11ea-9628-08482fe2ee20.png)
