import requests
from datetime import datetime

def get_weather_condition(code):

    weather_codes = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",

        45: "Fog",
        48: "Rime Fog",

        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",

        61: "Light Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",

        71: "Light Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",

        80: "Rain Showers",
        81: "Heavy Rain Showers",
        82: "Violent Rain Showers",

        95: "Thunderstorm"
    }

    return weather_codes.get(code, "Unknown")






def get_forecast(
    latitude,
    longitude,
    start_date,
    end_date
):
    url = "https://api.open-meteo.com/v1/forecast"


    response = requests.get(
        url,
        params={
            "latitude": latitude,
            "longitude":longitude,
            "daily":[
                "temperature_2m_max",
                "temperature_2m_min",
                "weather_code"
            ],

            "forecast_days":7
        }
    )

    data = response.json()

    daily = data["daily"]

    forecast = []

    for i, date_str in enumerate(daily["time"]):

        forecast_date = datetime.strptime(
            date_str,
            "%Y-%m-%d"
        ).date()

        if start_date <= forecast_date <= end_date:

            forecast.append({
                "date": date_str,
                "max_temp": daily["temperature_2m_max"][i],
                "min_temp": daily["temperature_2m_min"][i],
                "condition": get_weather_condition(
                    daily["weather_code"][i]
                )
            })

    return forecast




def get_weather(
    latitude,
    longitude
):

    url = "https://api.open-meteo.com/v1/forecast"

    response = requests.get(
        url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m"
            ]
        }
    )

    data = response.json()

    current = data["current"]

    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"]
    }

