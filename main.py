import os
import requests
import pycountry
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from collections import defaultdict
from datetime import datetime, timezone, timedelta

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
app = Flask(__name__)

def get_time_of_day(current_time, timezone_offset):
    local_time = (current_time + timezone_offset) % 86400
    local_hour = local_time // 3600

    if 5 <= local_hour < 6:
        return "sunrise"
    elif 18 <= local_hour < 20:
        return "sunset"
    elif 6 <= local_hour < 18:
        return "sunny"
    else:
        return "night"

def resolve_country_code(name):
    name = name.strip().lower()
    if len(name) == 2:
        return name.upper()
    try:
        country = pycountry.countries.search_fuzzy(name)[0]
        return country.alpha_2
    except LookupError:
        return name

def parse_city(city):
    parts = [p.strip() for p in city.split(",")]
    if len(parts) == 2:
        code = resolve_country_code(parts[1])
        return f"{parts[0]},{code}"
    return parts[0]

def get_current_weather(city):
    query = parse_city(city)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={API_KEY}&units=metric"
    response = requests.get(url, timeout=10)
    data = response.json()
    if response.status_code != 200:
        return None, data.get("message", "Something went wrong.")
    weather = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": round(data["main"]["temp"]),
        "feels_like": round(data["main"]["feels_like"]),
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind": data["wind"]["speed"],
        "description": data["weather"][0]["description"].capitalize(),
        "icon": data["weather"][0]["icon"],
        "time_of_day": get_time_of_day(data["dt"], data["timezone"]),
    }
    return weather, None

def get_forecast(city):
    query = parse_city(city)
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={query}&appid={API_KEY}&units=metric"
    response = requests.get(url, timeout=10)
    data = response.json()
    if response.status_code != 200:
        return []

    daily = defaultdict(list)
    for item in data["list"]:
        date = item["dt_txt"].split(" ")[0]
        daily[date].append(item)

    forecast = []
    for date, items in list(daily.items())[1:6]:
        temps = [i["main"]["temp"] for i in items]
        icons = [i["weather"][0]["icon"] for i in items]
        descriptions = [i["weather"][0]["description"] for i in items]
        forecast.append({
            "date": date,
            "min": round(min(temps)),
            "max": round(max(temps)),
            "icon": icons[len(icons)//2],
            "description": descriptions[len(descriptions)//2].capitalize(),
        })
    return forecast

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast = []
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if not city:
            error = "Please enter a city name."
        else:
            weather, error = get_current_weather(city)
            if weather:
                forecast = get_forecast(city)

    return render_template("index.html", weather=weather, forecast=forecast, error=error)

@app.route("/weather-by-coords")
def weather_by_coords():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url, timeout=10)
    data = response.json()
    return jsonify({"city": data["name"]})

if __name__ == "__main__":

    app.run(debug=True)