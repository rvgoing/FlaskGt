import io
import datetime  # Add this import
import requests
import matplotlib.pyplot as plt
from flask import Flask, Response


app = Flask(__name__)

# Define the API key at the beginning
API_KEY = 'e12e36503ebdefccbc6c4d8bf9a6158f'

@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask!</h1>'

@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name

@app.cli.command()
def hello():
    """Just say hello."""
    click.echo('Hello, Human!')

def check_api_key(api_key):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'lat': 25.0330,
        'lon': 121.5654,
        'appid': api_key
    }
    response = requests.get(url, params=params)
    return response.status_code == 200

def fetch_weather_data(api_key):
    lat, lon = 25.0330, 121.5654
    url = f'http://api.openweathermap.org/data/2.5/onecall/timemachine'
    temperatures = []
    humidities = []
    for i in range(1, 25):
        dt = int((datetime.datetime.utcnow() - datetime.timedelta(hours=i)).timestamp())
        params = {
            'lat': lat,
            'lon': lon,
            'dt': dt,
            'appid': api_key,
            'units': 'metric'
        }
        response = requests.get(url, params=params)
        data = response.json()
        if 'current' in data:
            temperatures.append(data['current'].get('temp', None))
            humidities.append(data['current'].get('humidity', None))
        else:
            temperatures.append(None)
            humidities.append(None)
    temperatures = [temp for temp in temperatures if temp is not None]
    humidities = [hum for hum in humidities if hum is not None]
    return temperatures, humidities
    


@app.route('/chart')
def chart():
    if not check_api_key(API_KEY):
        return '<h1>Invalid API key or the key is not live.</h1>'
    
    temperature, humidity = fetch_weather_data(API_KEY)
    hours = list(range(len(temperature)))

    # Create temperature chart
    plt.figure(figsize=(10, 5))
    plt.plot(hours, temperature, label='Temperature (°C)')
    plt.xlabel('Hours')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature in Taipei City (Past 24 Hours)')
    plt.legend()
    temp_img = io.BytesIO()
    plt.savefig(temp_img, format='png')
    temp_img.seek(0)
    plt.close()

    # Create humidity chart
    plt.figure(figsize=(10, 5))
    plt.plot(hours, humidity, label='Humidity (%)')
    plt.xlabel('Hours')
    plt.ylabel('Humidity (%)')
    plt.title('Humidity in Taipei City (Past 24 Hours)')
    plt.legend()
    hum_img = io.BytesIO()
    plt.savefig(hum_img, format='png')
    hum_img.seek(0)
    plt.close()

    return send_file(temp_img, mimetype='image/png'), send_file(hum_img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
