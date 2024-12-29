let map;

window.initMap = function() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 8,
    });
};

document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const location = document.getElementById('location-input').value;
    if (!location) {
        document.getElementById('error-message').textContent = 'Please enter a location.';
        return;
    }
    geocodeLocation(location);
});

function geocodeLocation(location) {
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: location }, function(results, status) {
        if (status === 'OK') {
            map.setCenter(results[0].geometry.location);
            fetchWeatherData(results[0].geometry.location.lat(), results[0].geometry.location.lng());
        } else {
            document.getElementById('error-message').textContent = 'Geocoding failed: ' + status;
        }
    });
}

function fetchWeatherData(lat, lon) {
    const url = `/weather?lat=${lat}&lon=${lon}`;
    fetch(url)
        .then(response => response.json())
        .then(data => updateWeatherInfo(data))
        .catch(error => console.error('Error fetching weather data:', error));
}

function updateWeatherInfo(data) {
    const weatherInfoDiv = document.getElementById('weather-info');
    weatherInfoDiv.innerHTML = `
        <p>Location: ${data.name}</p>
        <p>Temperature: ${data.temp}°C</p>
        <p>Weather: ${data.weather}</p>
        <p>Safety Score: ${data.safety_score}</p>
        <p>Frostbite Risk: ${data.frostbite_risk}</p>
    `;
}
