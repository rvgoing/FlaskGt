import requests
from flask import Flask, render_template, jsonify, request, send_file
import matplotlib.pyplot as plt
import io
from datetime import datetime  # Correct import for datetime class



app = Flask(__name__)

# 🔥 Replace with your actual OpenWeatherMap API key
API_KEY = "e12e36503ebdefccbc6c4d8bf9a6158f"

app = Flask(__name__)

@app.route('/')
def home():
    # return "Hello, Flask! Welcome to your simple demo."
    return render_template("index.html")  # ✅ Main Page (Hello Flask)


@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'Taipei')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from OpenWeatherMap"}), response.status_code

    weather_data = response.json()
    return jsonify(weather_data)

@app.route('/forecast', methods=['GET'])
def get_forecast():
    city = request.args.get('city', 'Taipei')
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from OpenWeatherMap"}), response.status_code

    forecast_data = response.json()
    return jsonify(forecast_data)

@app.route('/temperature_chart', methods=['GET'])
def temperature_chart():
    city = request.args.get('city', 'Taipei')
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from OpenWeatherMap"}), response.status_code

    forecast_data = response.json()
    city_name = forecast_data['city']['name']
    country = forecast_data['city']['country']
    full_city_name = f"{city_name}, {country}"

    return render_template('temperature.html', city=full_city_name)

@app.route('/temperature_chart_data', methods=['GET'])
def temperature_chart_data():
    city = request.args.get('city', 'Taipei')
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from OpenWeatherMap"}), response.status_code

    forecast_data = response.json()
    temperatures = [entry['main']['temp'] - 273.15 for entry in forecast_data['list']]  # Convert from Kelvin to Celsius
    times = [entry['dt_txt'].split(' ')[0] for entry in forecast_data['list']]  # Extract only the date part
    # times = [entry['dt_txt'] for entry in forecast_data['list']]


    return jsonify({'times': times, 'temperatures': temperatures})

    # Add the day of the week to the times
    # times_with_weekday = [f"{datetime.strptime(time, '%Y-%m-%d').strftime('%Y-%m-%d (%A)')}" for time in times]
    # return jsonify({'times': times_with_weekday, 'temperatures': temperatures})


@app.route('/humidity_chart', methods=['GET'])
def humidity_chart():
    city = request.args.get('city', 'Taipei')
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from OpenWeatherMap"}), response.status_code

    forecast_data = response.json()
    humidities = [entry['main']['humidity'] for entry in forecast_data['list']]
    times = [entry['dt_txt'] for entry in forecast_data['list']]

    plt.figure(figsize=(10, 5))
    plt.plot(times, humidities, marker='o')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Time')
    plt.ylabel('Humidity (%)')
    plt.title(f'Humidity Forecast for {city}')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
