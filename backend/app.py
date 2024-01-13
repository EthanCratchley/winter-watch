import requests
from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})  # This allows all origins for all routes

@app.route('/weather', methods=['GET'])
def get_weather():
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    api_key = 'key'  # Replace with your actual API key
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        # Assuming you're extracting temperature, lat, lon, and location name
        weather_data = {
            'temp': data['current']['temp'],
            'lat': data['lat'],
            'lon': data['lon'],
            'name': data['timezone']  # or other field representing location name
        }
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
