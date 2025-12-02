import os
import requests
from google.adk.agents import Agent

OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

def get_weather(location: str) -> dict:
    """
    Fetch current weather for `location` using OpenWeatherMap.
    Returns a dict with keys: city, temperature, description, humidity, weather.
    """
    if not OPENWEATHER_KEY:
        return {"error": "OPENWEATHER_KEY not set in environment (.env)"}

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": OPENWEATHER_KEY, "units": "metric"}

    try:
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json() 
    except requests.exceptions.RequestException as e:
        return {"error": f"Network/API error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

    # OpenWeather returns code in 'cod'
    if data.get("cod") != 200:
        msg = data.get("message", "unknown error")
        return {"error": f"OpenWeather error: {msg}"}

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    hum = data["main"].get("humidity")

    return {
        "city": data.get("name", location),
        "temperature": f"{temp}°C",
        "description": desc,
        "humidity": hum,
        "weather": f"{data.get('name', location)} is currently {desc} with {temp}°C and {hum}% humidity."
    }

root_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    description="Provides current weather using OpenWeatherMap API.",
    instruction="""
You are an AI assistant that answers weather questions. When the user asks about the current weather
for a city (examples: "What's the weather in Hyderabad?", "weather in London"), call the get_weather tool
with the city name and then give one concise, friendly sentence summarizing the returned information.
If the tool returns an error, tell the user that weather is unavailable and show the error message.
""",
    tools=[get_weather],
)

