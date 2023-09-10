from flask import Flask, request, jsonify, render_template, send_from_directory

import requests

app = Flask(__name__)

API_KEY = "8eaa9b435a8655b6d15c53f19e515965"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    
    if not city:
        return jsonify({'error': 'City name is required'}), 400

    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(weather_url)
    
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'weather_icon': data['weather'][0]['icon'],
        }
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'City not found'}), 404

@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    city = request.args.get('city')
    
    if not city:
        return jsonify({'error': 'City name is required'}), 400


    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(forecast_url)
    
    if response.status_code == 200:
        data = response.json()
        forecast_data = []

        for forecast_entry in data['list']:
            forecast_data.append({
                'date': forecast_entry['dt_txt'],
                'temperature': forecast_entry['main']['temp'],
                'description': forecast_entry['weather'][0]['description'],
            })

        return jsonify(forecast_data)
    else:
        return jsonify({'error': 'City not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
