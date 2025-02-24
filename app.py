import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 🔥 Replace with your actual OpenWeatherMap API key
API_KEY = "e12e36503ebdefccbc6c4d8bf9a6158f"

# Function to fetch weather data
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data["main"]["temp"] if "main" in data else None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather")
def weather_page():
    return render_template("weather.html")

@app.route("/api/weather")
def get_weather():
    cities = ["Taipei", "Brisbane", "Oulu"]
    data = {
        city: {
            "labels": ["Now"],  
            "temps": [get_weather_data(city)]  
        } for city in cities
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

