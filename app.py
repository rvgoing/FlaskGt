import io
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
    url = f'http://api.openweathermap.org/data/2.5/onecall/timemachine'
    params = {
        'lat': 25.0330,
        'lon': 121.5654,
        'dt': 'TIMESTAMP',
        'appid': api_key,
        'units': 'metric'
    }
    temperatures = []
    humidities = []
    for timestamp in [int((datetime.datetime.utcnow() - datetime.timedelta(hours=i)).timestamp()) for i in range(1, 25)]:
        params['dt'] = timestamp
        response = requests.get(url, params=params)
        data = response.json()
        temperatures.append(data['current']['temp'])
        humidities.append(data['current']['humidity'])
    return temperatures, humidities

@app.route('/chart')
def chart():
    temperature, humidity = fetch_weather_data()
    hours = list(range(24))

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
