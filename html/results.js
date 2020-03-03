function displayMarkers(inp,clusterGroup,min=-1,max=-1) {
    inp.forEach(element => {
        var marker = L.marker([element.lat, element.lon]);
        if((min == -1 || element.price >= min) && 
            (max == -1 || element.price <= max)) {
                clusterGroup.addLayer(marker);
                var content = `
                <p> <a href="${element.link}" target="_blank">${element.title}</a> </p>
                <p> Price: ${element.price} </p>
                `
                marker.bindPopup(content);
            }
    });
}

var minPrice = -1;
var maxPrice = -1;

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
    let id = 0
    displayMarkers(data,markersClusterGroup);

    mymap.addLayer(markersClusterGroup);

    $("#minPrice").change(event => {
        let value = event.currentTarget.value;
        minPrice = value;
        markersClusterGroup.clearLayers();
        displayMarkers(data,markersClusterGroup,minPrice,maxPrice);
    });
    $("#maxPrice").change(event => {
        let value = event.currentTarget.value;
        maxPrice = value;
        markersClusterGroup.clearLayers();
        displayMarkers(data,markersClusterGroup,minPrice,maxPrice);
    });

});