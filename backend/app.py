import requests
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})  # This allows all origins for all routes


def calculate_safety_score(weather_data):
    score = 100
    score -= max(0, (30 - weather_data['temp']) * 2)  # Subtract more points for lower temperatures
    score -= max(0, (10000 - weather_data['visibility']) // 1000)  # Points for lower visibility
    score -= max(0, weather_data['uv_index'] * 2)  # UV index factor
    if weather_data['weather'].lower() in ['rain', 'snow', 'thunderstorm']:
        score -= 20  # Bad weather conditions
    return max(0, int(score))  # Convert to integer and ensure score is not negative

def calculate_frostbite_indicator(weather_data):
    temp = weather_data['temp']
    wind_speed = weather_data.get('wind_speed', 0)  # Add wind_speed to weather_data if not present
    if temp < 0 and wind_speed > 20:
        return 'High'
    elif temp < 0:
        return 'Moderate'
    return 'Low'

@app.route('/weather', methods=['GET'])
def get_weather():
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()
    #print(data)  # Add this line to debug

    if response.status_code == 200:
        current_data = data['current']
        hourly_data = data.get('hourly', [])

        # Find the most recent snow forecast (simplified approach)
        last_snow = None
        for hour in hourly_data:
           weather = hour['weather'][0]
           if weather['main'].lower() == 'snow':
               last_snow_time = datetime.fromtimestamp(hour['dt'])
               last_snow = last_snow_time.strftime("%Y-%m-%d %H:%M:%S")
               break  # Stop after finding the first recent snow

        weather_data = {
            'temp': current_data['temp'],
            'lat': data['lat'],
            'lon': data['lon'],
            'name': data['timezone'],  # Using timezone as the location name
            'time': datetime.now().strftime("%H:%M:%S"),  # Current server time
            'date': datetime.now().strftime("%Y-%m-%d"),  # Current server date
            'weather': current_data['weather'][0]['main'],  # Current weather condition
            'uv_index': current_data['uvi'],
            'visibility': current_data['visibility'],
            'ice_warning': 'Yes' if current_data['temp'] < 0 else 'No',
            'last_snow': last_snow if last_snow else "No recent snow"
        }
        weather_data['safety_score'] = calculate_safety_score(weather_data)
        weather_data['frostbite_risk'] = calculate_frostbite_indicator(weather_data)

        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
