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

    var markersClusterGroup = L.markerClusterGroup({disableClusteringAtZoom: 15});
    var displayedMarkers = []
    let id = 0
    data.forEach(element => {
        var marker = L.marker([element.lat, element.lon]);
        markersClusterGroup.addLayer(marker);
        var content = `
        <p> Title: ${element.title} </p>
        <p> Price: ${element.price} </p>
        <p> <a href="${element.link}">kijiji link</a> </p>
        `
        marker.bindPopup(content);
        displayedMarkers.push(id)
    });

    mymap.addLayer(markersClusterGroup);

});