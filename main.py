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
    local_dt = datetime.fromtimestamp(current_time, tz=timezone.utc) + timedelta(seconds=timezone_offset)
    local_hour = local_dt.hour

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
        "sunrise": data["sys"]["sunrise"],
        "sunset": data["sys"]["sunset"],
        "current_time": data["dt"],
        "timezone_offset": data["timezone"],
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"],
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
            "date": datetime.strptime(date, "%Y-%m-%d").strftime("%a, %b %d"),
            "min": round(min(temps)),
            "max": round(max(temps)),
            "icon": icons[len(icons)//2],
            "description": descriptions[len(descriptions)//2].capitalize(),
        })
    return forecast

def get_air_quality(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url, timeout=10)
    data = response.json()
    if response.status_code != 200:
        return None
    
    components = data["list"][0]["components"]
    pm25 = components["pm2_5"]

    # Convert PM2.5 to US AQI
    def pm25_to_aqi(pm):
        breakpoints = [
            (0, 12.0, 0, 50),
            (12.1, 35.4, 51, 100),
            (35.5, 55.4, 101, 150),
            (55.5, 150.4, 151, 200),
            (150.5, 250.4, 201, 300),
            (250.5, 500.4, 301, 500),
        ]
        for lo_pm, hi_pm, lo_aqi, hi_aqi in breakpoints:
            if lo_pm <= pm <= hi_pm:
                return round((hi_aqi - lo_aqi) / (hi_pm - lo_pm) * (pm - lo_pm) + lo_aqi)
        return 500

    aqi_value = pm25_to_aqi(pm25)

    if aqi_value <= 50:
        label, color = "Good", "#00e400"
    elif aqi_value <= 100:
        label, color = "Moderate", "#ffff00"
    elif aqi_value <= 150:
        label, color = "Poor", "#ff7e00"
    elif aqi_value <= 200:
        label, color = "Unhealthy", "#ff0000"
    elif aqi_value <= 300:
        label, color = "Severe", "#8f3f97"
    else:
        label, color = "Hazardous", "#7e0023"

    return {
        "aqi": aqi_value,
        "label": label,
        "color": color,
        "percent": min(aqi_value / 500 * 100, 100),
        "pm25": round(pm25, 1),
        "pm10": round(components["pm10"], 1),
        "no2": round(components["no2"], 1),
        "o3": round(components["o3"], 1),
    }

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast = []
    error = None
    aqi = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if not city:
            error = "Please enter a city name."
        else:
            weather, error = get_current_weather(city)
            if weather:
                forecast = get_forecast(city)
                aqi = get_air_quality(weather["lat"], weather["lon"])

    return render_template("index.html", weather=weather, forecast=forecast, error=error, aqi=aqi)

@app.route("/weather-by-coords")
def weather_by_coords():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Missing coordinates"}), 400
    try:
        lat, lon = float(lat), float(lon)
    except ValueError:
        return jsonify({"error": "Invalid coordinates"}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url, timeout=10)
    data = response.json()

    if response.status_code != 200:
        return jsonify({"error": data.get("message", "Could not fetch weather")}), 502

    return jsonify({"city": data["name"]})


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")