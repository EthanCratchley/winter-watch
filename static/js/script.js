let map;

// Function to initialize the map
function initMap() {
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
            // Fetch weather data for the geocoded location
            fetchWeatherData(results[0].geometry.location.lat(), results[0].geometry.location.lng());
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

// Function to fetch weather data from Flask backend
function fetchWeatherData(lat, lon) {
    const url = `${window.location.origin}/weather?lat=${lat}&lon=${lon}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            updateWeatherInfo(data); 
        })
        .catch(error => console.error('Error fetching weather data:', error));
}
// Function to update UI with weather data
function updateWeatherInfo(data) {
    document.getElementById('temperature-value').textContent = data.temp;
    document.getElementById('location-value').textContent = data.name;
    document.getElementById('display-lon').textContent = data.lon;
    document.getElementById('display-lat').textContent = data.lat;
    document.getElementById('time-value').textContent = data.time;
    document.getElementById('date-value').textContent = data.date;
    document.getElementById('weather-value').textContent = data.weather;
    document.getElementById('uv-index-value').textContent = data.uv_index;
    document.getElementById('visibility-rating-value').textContent = `${data.visibility} meters`;
    document.getElementById('ice-warning-value').textContent = data.ice_warning;
    document.getElementById('last-snow-value').textContent = data.last_snow;
    document.getElementById('safety-score').textContent =  data.safety_score;
    document.getElementById('frostbite-risk').textContent = data.frostbite_risk;
}

// Event listener for the form submission
document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault(); 
    const location = document.getElementById('location-input').value;
    geocodeLocation(location); 
});
