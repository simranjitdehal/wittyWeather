from flask import Blueprint, request, jsonify
import requests
import os
from utils import generate_humor
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

weather_bp = Blueprint("weather", __name__)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@weather_bp.route("/get_weather", methods=["GET"])
@jwt_required()
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "Please provide a city name"}), 400

    # Call OpenWeather API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({"error": "City not found"}), 404
    
    data = response.json()
    
    weather_info = {
        "city": city,
        "temp": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "feels_like": data["main"]["feels_like"],
        "clouds": data["clouds"]["all"]
    }

    # Generate humor
    funny_comments = generate_humor(weather_info)

    return jsonify({
    "city": city,
    "temperature": weather_info["temp"],
    "description": weather_info["description"],
    "humidity": weather_info["humidity"],
    "wind_speed": weather_info["wind_speed"],
    "feels_like": weather_info["feels_like"],
    "funny_temperature": funny_comments["temperature"],
    "funny_humidity": funny_comments["humidity"],
    "funny_wind": funny_comments["wind"],
    "cloudiness": weather_info["clouds"],
    "funny_clouds": funny_comments["clouds"]
})