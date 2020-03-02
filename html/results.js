$(document).ready(() => {
    var mymap = L.map('mapid').setView([43.8524, -79.4162], 11);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: token
    }).addTo(mymap);

    var markers = {}
    var displayedMarkers = []
    let id = 0
    data.forEach(element => {
        var marker = L.marker([element.lat, element.lon]).addTo(mymap);
        var content = `
        <p> Title: ${element.title} </p>
        <p> Price: ${element.price} </p>
        <p> <a href="${element.link}">kijiji link</a> </p>
        `
        marker.bindPopup(content);
        markers[id++] = marker;
        displayedMarkers.push(id)
    });

    mymap.on('moveend', function(e) {

        // Get boundaries of new view
        var bounds = mymap.getBounds();
        var north = bounds.getNorth();
        var south = bounds.getSouth();
        var east = bounds.getEast();
        var west = bounds.getWest();

        var toShow = []
        var toHide = []
        Object.keys(markers).forEach((id) => {
            let element = markers[id]
            let lat = element.getLatLng().lat;
            let lng = element.getLatLng().lng;
            if(lat > north ||
                lat < south ||
                lng > east ||
                lng < west) toHide.push(id)
            else toShow.push(id)
        });
        console.log("Hiding: " + toHide.length);
        console.log("Showing: " + toShow.length);
        if(toShow.length > 1000) {
            toShow = toShow.slice(1,1000);
            console.log("Limiting to 2000 entries");
        }
        toHide.forEach(id => {
            mymap.removeLayer(markers[id])
        });
        toShow.forEach(id => {
            let marker = markers[id]
            if(!mymap.hasLayer(marker)) mymap.addLayer(marker)
        })

        
    });

});