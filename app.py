import requests
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/weather": {"origins": "*"}})  # Adjust origin in production

# Validate API keys
OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

if not OPENWEATHERMAP_API_KEY:
    raise ValueError("OPENWEATHERMAP_API_KEY is not set in the environment variables")

if not GOOGLE_MAPS_API_KEY:
    raise ValueError("GOOGLE_MAPS_API_KEY is not set in the environment variables")


def calculate_safety_score(weather_data):
    score = 100
    score -= max(0, (30 - weather_data['temp']) * 2)  # Penalize for cold temperatures
    score -= max(0, (10000 - weather_data['visibility']) // 1000)  # Penalize for low visibility
    score -= max(0, weather_data['uv_index'] * 2)  # Penalize for high UV index
    if weather_data['weather'].lower() in ['rain', 'snow', 'thunderstorm']:
        score -= 20  # Penalize for severe weather
    return max(0, int(score))  # Ensure score doesn't go below 0


def calculate_frostbite_indicator(weather_data):
    temp = weather_data['temp']
    wind_speed = weather_data.get('wind_speed', 0)  # Default wind speed to 0 if missing
    if temp < 0 and wind_speed > 20:
        return 'High'
    elif temp < 0:
        return 'Moderate'
    return 'Low'


@app.route('/weather', methods=['GET'])
def get_weather():
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')

    if not latitude or not longitude:
        return jsonify({'error': 'Latitude and longitude are required parameters'}), 400

    api_key = OPENWEATHERMAP_API_KEY
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from OpenWeatherMap'}), response.status_code

    data = response.json()
    if 'current' not in data:
        return jsonify({'error': 'Invalid data format received from OpenWeatherMap'}), 500

    current_data = data['current']
    hourly_data = data.get('hourly', [])

    # Calculate last snow time
    last_snow = None
    for hour in hourly_data:
        weather = hour.get('weather', [{}])[0]
        if weather.get('main', '').lower() == 'snow':
            last_snow_time = datetime.fromtimestamp(hour['dt'])
            last_snow = last_snow_time.strftime("%Y-%m-%d %H:%M:%S")
            break

    # Construct the weather data object
    weather_data = {
        'temp': current_data['temp'],
        'lat': data['lat'],
        'lon': data['lon'],
        'name': data.get('timezone', 'Unknown Location'),
        'time': datetime.now().strftime("%H:%M:%S"),
        'date': datetime.now().strftime("%Y-%m-%d"),
        'weather': current_data['weather'][0]['main'],
        'uv_index': current_data.get('uvi', 0),
        'visibility': current_data.get('visibility', 10000),  # Default to max visibility
        'ice_warning': 'Yes' if current_data['temp'] < 0 else 'No',
        'last_snow': last_snow if last_snow else "No recent snow"
    }

    # Add calculated metrics
    weather_data['safety_score'] = calculate_safety_score(weather_data)
    weather_data['frostbite_risk'] = calculate_frostbite_indicator(weather_data)

    return jsonify(weather_data)


@app.route('/')
def index():
    google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    return render_template('index.html', google_maps_api_key=google_maps_api_key)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=False)
