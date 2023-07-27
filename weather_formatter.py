from weather_api_service import Weather

def format_weather(weather: Weather) -> str:
    weather_text = f"{weather.city}, температура {weather.temperature}°C, {weather.weather_type}\n" \
                   f"Восход: {weather.sunrise}\n" \
                   f"Закат: {weather.sunset}"
    return weather_text
