import requests
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})  # This allows all origins for all routes

@app.route('/weather', methods=['GET'])
def get_weather():
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    api_key = '3c6ecea3f0340c19cb44075ac83a0560'  # Replace with your actual API key
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
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
