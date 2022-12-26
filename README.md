# Kijiji Mappifier

I created this tool after I moved to Toronto and was looking for a place to rent. Since Kijiji has no map feature when looking for appartments to rent, this tool scrapes the result pages of Kijiji, finds the price and location of the appartments, and stores them in a CSV database. It then uses [LocationIQ](https://locationiq.com/) API to get the coordinates of each address. Finally, [Leafletjs](https://leafletjs.com/) API is used to display the results on a map.

## Prerequisits

* `node` and `yarn` installed in the `PATH`
* [LocationIQ](https://locationiq.com/) token
* [Leafletjs](https://leafletjs.com/) token

## How to use

1. Export `LOCATION_IQ_TOKEN` to your LocationIQ token and `LEAFLET_TOKEN` to your LeafletJs token.
2. Run the backend: `cd packages/backend; node index.js`. The backend will generate a _frontend/data.json_ file that contains the data needed to be rendered in the frontend map. It will also create a _frontend/token.js_ that includes the leaflet token, this will be used by the frontend to show a map.
3. Open _frontend/index.html_ in a browser to view the results

## Screenshots of the result

* ![screenshot1](https://user-images.githubusercontent.com/12204690/75831760-63387f00-5d82-11ea-8693-81547269e25d.png)

* ![screenshot2](https://user-images.githubusercontent.com/12204690/75831751-5b78da80-5d82-11ea-9a25-e89695df0ac9.png)

* ![screenshot3](https://user-images.githubusercontent.com/12204690/75831768-6df31400-5d82-11ea-80a1-dd8f3139cfc6.png)

* ![screenshot4](https://user-images.githubusercontent.com/12204690/75831783-7c413000-5d82-11ea-9628-08482fe2ee20.png)
