from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

API_KEY = "e12e36503ebdefccbc6c4d8bf9a6158f"  # Replace with your API Key
CITY = "Taipei"

@app.route("/")
def home():
    return render_template("weather.html")

@app.route("/api/weather")
def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    # Extract temperature data for the next 8 time slots
    labels = [item["dt_txt"] for item in data["list"][:18]]
    temps = [item["main"]["temp"] for item in data["list"][:18]]

    return jsonify({"labels": labels, "temps": temps})

if __name__ == "__main__":
    app.run(debug=True)
