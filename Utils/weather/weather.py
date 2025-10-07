"""
utils/weather/weather.py
------------------------
Weather fetching module for TARS using OpenWeatherMap API.
"""

import os
import requests
from dotenv import load_dotenv

# Load .env to fetch API key
load_dotenv()

# You can hardcode or pull from .env
API_KEY = os.getenv("WEATHER_API")

def get_weather(city: str = "San Jose") -> str:
    """
    Fetch current weather data for a given city using OpenWeatherMap API.
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data.get("cod") != 200:
            return f"⚠️ Sorry, I couldn't find weather info for {city}."

        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        desc = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        return (
            f"The weather in {city} is currently {desc}. "
            f"Temperature: {temp}°C (feels like {feels}°C), "
            f"humidity {humidity}%, and wind speed {wind} m/s."
        )

    except Exception as e:
        return f"❌ Error fetching weather: {e}"
