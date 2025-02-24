from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

API_KEY = "e12e36503ebdefccbc6c4d8bf9a6158f"  # Replace with your API Key

CITIES = {
    "Taipei": "Taipei",
    "Brisbane": "Brisbane",
    "Oulu": "Oulu"
}

@app.route("/")
def home():
    return render_template("weather.html")

@app.route("/api/weather")
def get_weather():
    data_dict = {}

    for city_name, city in CITIES.items():
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        labels = [item["dt_txt"] for item in data["list"][:80]]
        temps = [item["main"]["temp"] for item in data["list"][:80]]

        data_dict[city_name] = {"labels": labels, "temps": temps}

    return jsonify(data_dict)

if __name__ == "__main__":
    app.run(debug=True)
