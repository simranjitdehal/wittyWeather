import random
from jokes import temp_jokes, wind_jokes, humidity_jokes, cloud_jokes

# Helper function to pick a random joke based on value
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

# Generate full humorous comment
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
