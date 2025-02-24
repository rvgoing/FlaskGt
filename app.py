import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 🔥 Replace with your actual OpenWeatherMap API key
API_KEY = "e12e36503ebdefccbc6c4d8bf9a6158f"


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather")
def weather_page():
    return render_template("weather.html")


# ==
@app.route("/api/weather")
def get_weather():
    data_dict = {}

    for city in CITIES:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        labels = [item["dt_txt"] for item in data["list"][:8]]  # Next 8 time slots
        temps = [item["main"]["temp"] for item in data["list"][:8]]

        data_dict[city] = {"labels": labels, "temps": temps}

    return jsonify(data_dict)
# ==


if __name__ == "__main__":
    app.run(debug=True)

