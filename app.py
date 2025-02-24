import requests
from flask import Flask, render_template, jsonify, request  # ✅ Fix: Import `request`

app = Flask(__name__)

# 🔥 Replace with your actual OpenWeatherMap API key
API_KEY = "e12e36503ebdefccbc6c4d8bf9a6158f"

# Function to fetch weather forecast data
def get_weather_data(city, tslot=10):  # Default `tslot` = 10
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if "list" in data:
        timestamps = [entry["dt_txt"].split(" ")[1] for entry in data["list"][:tslot]]  # First `tslot` time slots
        temperatures = [entry["main"]["temp"] for entry in data["list"][:tslot]]  # First `tslot` temperatures
        return {"labels": timestamps, "temps": temperatures}
    else:
        return {"labels": [], "temps": []}  # Return empty if API fails

@app.route("/")
def home():
    return render_template("index.html")  # ✅ Main Page (Hello Flask)

@app.route("/weather")
def weather_page():
    return render_template("weather.html")  # ✅ Weather Page (with chart)

@app.route("/api/weather")
def get_weather():
    cities = ["Taipei", "Brisbane", "Oulu"]  # ✅ Cities for weather data
    tslot = request.args.get("tslot", default=10, type=int)  # ✅ Get `tslot` from URL, default=10
    data = {city: get_weather_data(city, tslot) for city in cities}
    return jsonify(data)  # ✅ Return weather data as JSON

if __name__ == "__main__":
    app.run(debug=True)
