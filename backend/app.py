from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from config import OPENWEATHER_API_KEY
from jokes import temp_jokes, wind_jokes, humidity_jokes, cloud_jokes
import random

app = Flask(__name__)
CORS(app)

# ------------------------
# Helper function to pick a random joke based on value
# ------------------------
def choose_joke(value, jokes_dict):
    for key in jokes_dict:
        if key.startswith("<") and value < int(key[1:]):
            return random.choice(jokes_dict[key])
        elif "-" in key:
            low, high = map(int, key.split("-"))
            if low <= value <= high:
                return random.choice(jokes_dict[key])
        elif key.startswith(">") and value > int(key[1:]):
            return random.choice(jokes_dict[key])
    # fallback if no match
    return "😎 Weather vibes in your city!"

# ------------------------
# Generate full humorous comment
# ------------------------
def generate_humor(weather_data):
    temp_joke = choose_joke(weather_data["temp"], temp_jokes).format(
        city=weather_data["city"], temp=weather_data["temp"]
    )
    humidity_joke = choose_joke(weather_data["humidity"], humidity_jokes).format(
        city=weather_data["city"], humidity=weather_data["humidity"]
    )
    wind_joke = choose_joke(weather_data["wind_speed"], wind_jokes).format(
        city=weather_data["city"], wind_speed=weather_data["wind_speed"]
    )
    cloud_joke = choose_joke(weather_data.get("clouds", 0), cloud_jokes).format(
        city=weather_data["city"], cloudiness=weather_data.get("clouds", 0)
    )

    # Return as a list or dictionary if you want separate fields
    return {
        "temperature": temp_joke,
        "humidity": humidity_joke,
        "wind": wind_joke,
        "clouds": cloud_joke
    }



# ------------------------
# Flask routes
# ------------------------
@app.route("/")
def home():
    return "WittyWeather backend is running!"

@app.route("/get_weather", methods=["GET"])
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

if __name__ == "__main__":
    app.run(debug=True)
