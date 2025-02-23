import io
import datetime  # Add this import
import requests
import matplotlib.pyplot as plt
from flask import Flask, Response


app = Flask(__name__)

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

def fetch_weather_data():
    api_key = '98d3e2789160b7e80590153f2451c490'
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
    temperature, humidity = fetch_weather_data()
    hours = list(range(len(temperature)))

    plt.figure(figsize=(10, 5))
    plt.plot(hours, temperature, label='Temperature (°C)')
    plt.plot(hours, humidity, label='Humidity (%)')
    plt.xlabel('Hours')
    plt.ylabel('Values')
    plt.title('Temperature and Humidity in Taipei City (Past 24 Hours)')
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return Response(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
