import os
import streamlit as st
import requests
from datetime import datetime, timedelta

# Constants
API_KEY = os.getenv("WEATHER_API_KEY", "your_api_key_here")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CACHE_EXPIRY_MINUTES = 10

# Cache for weather data
weather_cache = {}

def get_weather_data(location):
    """Fetch weather data from OpenWeatherMap API."""
    if location in weather_cache:
        cached_data, timestamp = weather_cache[location]
        if datetime.now() - timestamp < timedelta(minutes=CACHE_EXPIRY_MINUTES):
            return cached_data

    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        weather_cache[location] = (data, datetime.now())
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def display_weather(data):
    """Display weather data in the UI."""
    if not data:
        return

    location = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]
    icon = data["weather"][0]["icon"]

    st.title(f"Weather in {location}, {country}")
    st.image(f"https://openweathermap.org/img/wn/{icon}@2x.png", width=100)
    st.write(f"Temperature: {temp}°C (Feels like {feels_like}°C)")
    st.write(f"Humidity: {humidity}%")
    st.write(f"Conditions: {description.capitalize()}")

def main():
    st.title("Weather App")
    location = st.text_input("Enter location:", "London")

    if st.button("Get Weather"):
        with st.spinner("Fetching weather data..."):
            weather_data = get_weather_data(location)
            if weather_data:
                display_weather(weather_data)

if __name__ == "__main__":
    main()
