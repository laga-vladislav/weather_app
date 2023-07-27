from datetime import datetime
from typing import NamedTuple
from enum import Enum
import json
from json.decoder import JSONDecodeError
from http.client import HTTPResponse
from urllib.error import URLError
from urllib.request import urlopen

from coordinates import Coordinates
from config import OPEN_WEATHER_URL
from expections import ApiServiceError

Celsius = int

class WeatherType(Enum):
    THUNDERSTORM = 'Гроза'
    DRIZZLE = 'Изморозь'
    RAIN = 'Дождь'
    SNOW = 'Снег'
    FOG = 'Туман'
    CLEAR = 'Ясно'
    CLOUDS = 'Облачно'


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str

def get_weather(coordinates: Coordinates) -> Weather:
    """Returns weather from OpenWeather API"""
    response = _get_response(latitude=coordinates.latitude,
                             longitude=coordinates.longitude)
    dict_response = _get_dict_response(response)
    return Weather(
        temperature=_parse_temperature(dict_response),
        weather_type=_parse_weather_type(dict_response),
        sunrise=_parse_sun_time(dict_response, 'sunrise'),
        sunset=_parse_sun_time(dict_response, 'sunset'),
        city=_parse_city(dict_response)
    )

def _get_response(latitude: float, longitude: float) -> HTTPResponse:
    try:
        url = OPEN_WEATHER_URL.format(latitude=latitude,
                                      longitude=longitude)
        return urlopen(url)
    except URLError:
        raise ApiServiceError

def _get_dict_response(response: HTTPResponse) -> dict:
    try:
        return json.load(response)
    except JSONDecodeError:
        raise ApiServiceError

def _parse_temperature(dict_response: dict) -> Celsius:
    temp = dict_response['main']['temp']
    return Celsius(temp)

def _parse_weather_type(dict_response: dict) -> WeatherType:
    weather_types = {
        'Thunderstorm': WeatherType.THUNDERSTORM,
        'Drizzle': WeatherType.DRIZZLE,
        'Rain': WeatherType.RAIN,
        'Snow': WeatherType.SNOW,
        'Atmosphere': WeatherType.FOG,
        'Clear': WeatherType.CLEAR,
        'Clouds': WeatherType.CLOUDS
    }
    try:
        parsed_weather_type = str(dict_response['weather'][0]['main'])
        weather_type = weather_types[parsed_weather_type]
        if weather_type is None:
            raise ApiServiceError
        return weather_type.value
    except TypeError:
        raise ApiServiceError

def _parse_sun_time(
        dict_response: dict,
        time: str) -> datetime:
    if time not in ["sunrise", "sunset"]:
        raise ApiServiceError
    return datetime.fromtimestamp(dict_response['sys'][time]).strftime("%H:%M:%S")

def _parse_city(dict_response: dict) -> str:
    return dict_response['name']


if __name__ == "__main__":
    weather = get_weather(
        Coordinates(longitude=float(127), latitude=float(50))
    )
    print(weather)
