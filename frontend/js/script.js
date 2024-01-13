let map;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 43.651070, lng: -79.347015 }, // Toronto Default Location 43.6532° N, 79.3832° W
        zoom: 10
    });
}

document.getElementById('search-button').addEventListener('click', function() {
    var geocoder = new google.maps.Geocoder();
    var address = document.getElementById('location-input').value;

    geocoder.geocode({'address': address}, function(results, status) {
        if (status === 'OK') {
            map.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location
            });
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
});
