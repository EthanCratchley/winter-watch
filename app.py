import requests
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from flask import send_from_directory
from flask import render_template

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})  

def calculate_safety_score(weather_data):
    score = 100
    score -= max(0, (30 - weather_data['temp']) * 2)  
    score -= max(0, (10000 - weather_data['visibility']) // 1000)  
    score -= max(0, weather_data['uv_index'] * 2)  
    if weather_data['weather'].lower() in ['rain', 'snow', 'thunderstorm']:
        score -= 20  
    return max(0, int(score))  

def calculate_frostbite_indicator(weather_data):
    temp = weather_data['temp']
    wind_speed = weather_data.get('wind_speed', 0) 
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

    if response.status_code == 200:
        current_data = data['current']
        hourly_data = data.get('hourly', [])

        last_snow = None
        for hour in hourly_data:
           weather = hour['weather'][0]
           if weather['main'].lower() == 'snow':
               last_snow_time = datetime.fromtimestamp(hour['dt'])
               last_snow = last_snow_time.strftime("%Y-%m-%d %H:%M:%S")
               break  

        weather_data = {
            'temp': current_data['temp'],
            'lat': data['lat'],
            'lon': data['lon'],
            'name': data['timezone'],  
            'time': datetime.now().strftime("%H:%M:%S"), 
            'date': datetime.now().strftime("%Y-%m-%d"), 
            'weather': current_data['weather'][0]['main'],  
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
