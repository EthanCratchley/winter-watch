// Assume a global variable for the map is declared
let map;

// Function to initialize the map
function initMap() {
    // Set the default location to Toronto for example
    const defaultLocation = { lat: 43.65107, lng: -79.347015 };
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: defaultLocation
    });
}

// Function to geocode a location and update the map
function geocodeLocation(location) {
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'address': location }, function(results, status) {
        if (status === 'OK') {
            map.setCenter(results[0].geometry.location);
            new google.maps.Marker({
                map: map,
                position: results[0].geometry.location
            });
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

// Event listener for the form submission
document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way
    const location = document.getElementById('location-input').value;
    geocodeLocation(location); // Call the function to update the map
});
